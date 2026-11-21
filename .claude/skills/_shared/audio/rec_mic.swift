// rec_mic: record the Mac's default input (Dan's desk Yeti) to 16-bit WAV segments without dropping audio.
// Why not ffmpeg: `ffmpeg -f avfoundation -i ":0"` keeps one audio buffer at a time and silently drops the rest when the
// machine is busy. Measured 2026-10-12 with one other build running: 26.6 s of samples per 30 s of wall time (11 % lost),
// a missing 512-sample block about every 90 ms, in three recordings out of three. Whisper still transcribes it, so nothing fails.
//   swiftc -O rec_mic.swift -o ~/.cache/absbyai/rec_mic
//   rec_mic OUT_DIR MAX_SECONDS [SEGMENT_SECONDS=30]     writes OUT_DIR/seg_000.wav, seg_001.wav ...; stops early when OUT_DIR/STOP exists
// The open segment is part_NNN.wav (AVAudioFile picks the container from the extension, so it must end in .wav).
// Each finished segment is a complete file (readable while the recorder keeps running). Prints one line per segment.
import AVFoundation
let a = CommandLine.arguments
guard a.count >= 3, let maxS = Double(a[2]) else { print("usage: rec_mic OUT_DIR MAX_SECONDS [SEGMENT_SECONDS]"); exit(2) }
let dir = a[1]; let segS = a.count > 3 ? (Double(a[3]) ?? 30) : 30
try? FileManager.default.createDirectory(atPath: dir, withIntermediateDirectories: true)
let engine = AVAudioEngine(); let input = engine.inputNode; let fmt = input.outputFormat(forBus: 0)
let settings: [String: Any] = [AVFormatIDKey: kAudioFormatLinearPCM, AVSampleRateKey: fmt.sampleRate, AVNumberOfChannelsKey: fmt.channelCount,
                               AVLinearPCMBitDepthKey: 16, AVLinearPCMIsFloatKey: false, AVLinearPCMIsBigEndianKey: false]
var file: AVAudioFile? = nil; var k = 0; var inSeg: AVAudioFramePosition = 0; var total: AVAudioFramePosition = 0
func open() { let p = String(format: "%@/part_%03d.wav", dir, k); file = try? AVAudioFile(forWriting: URL(fileURLWithPath: p), settings: settings, commonFormat: fmt.commonFormat, interleaved: fmt.isInterleaved); inSeg = 0 }
func close() {
    guard file != nil else { return }
    file = nil                                                            // deinit finalises the header
    try? FileManager.default.moveItem(atPath: String(format: "%@/part_%03d.wav", dir, k), toPath: String(format: "%@/seg_%03d.wav", dir, k))
    print(String(format: "seg_%03d.wav %.2f s", k, Double(inSeg) / fmt.sampleRate)); fflush(stdout); k += 1
}
open()
input.installTap(onBus: 0, bufferSize: 4096, format: fmt) { buf, _ in
    try? file?.write(from: buf); inSeg += AVAudioFramePosition(buf.frameLength); total += AVAudioFramePosition(buf.frameLength)
    if Double(inSeg) >= segS * fmt.sampleRate { close(); open() }
}
do { try engine.start() } catch { print("could not start the microphone: \(error)"); exit(1) }
print("recording \(fmt.sampleRate) Hz, \(fmt.channelCount) ch"); fflush(stdout)
let t0 = Date()
while Date().timeIntervalSince(t0) < maxS && !FileManager.default.fileExists(atPath: dir + "/STOP") { RunLoop.current.run(until: Date().addingTimeInterval(0.25)) }
engine.stop(); input.removeTap(onBus: 0); close()
print(String(format: "done: %.2f s of samples in %.2f s of wall time", Double(total) / fmt.sampleRate, Date().timeIntervalSince(t0)))
