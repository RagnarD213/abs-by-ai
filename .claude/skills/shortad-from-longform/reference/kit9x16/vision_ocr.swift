// Apple Vision text recognition for kit9x16/auto_content.py. Free, on-device.
// usage: vision_ocr <image> [<image> ...]  ->  one JSON object per line:
//   {"image": path, "lines": [{"text": s, "conf": c, "box": [x0, y0, x1, y1]}]}   (box in pixels, top-left origin)
import Foundation
import Vision
import AppKit

func esc(_ s: String) -> String {
    var o = ""
    for ch in s.unicodeScalars {
        switch ch {
        case "\"": o += "\\\""
        case "\\": o += "\\\\"
        case "\n": o += "\\n"
        default:
            if ch.value < 0x20 { o += String(format: "\\u%04x", ch.value) } else { o.unicodeScalars.append(ch) }
        }
    }
    return o
}

for path in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        print("{\"image\": \"\(esc(path))\", \"error\": \"unreadable\", \"lines\": []}")
        continue
    }
    let W = Double(cg.width), H = Double(cg.height)
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = true
    req.recognitionLanguages = ["en-US"]
    let h = VNImageRequestHandler(cgImage: cg, options: [:])
    try? h.perform([req])
    var parts: [String] = []
    for o in (req.results ?? []) {
        guard let c = o.topCandidates(1).first else { continue }
        let b = o.boundingBox
        let x0 = b.minX * W, x1 = b.maxX * W, y0 = (1 - b.maxY) * H, y1 = (1 - b.minY) * H
        parts.append(String(format: "{\"text\": \"%@\", \"conf\": %.3f, \"box\": [%.1f, %.1f, %.1f, %.1f]}",
                            esc(c.string), c.confidence, x0, y0, x1, y1))
    }
    print("{\"image\": \"\(esc(path))\", \"lines\": [\(parts.joined(separator: ", "))]}")
}
