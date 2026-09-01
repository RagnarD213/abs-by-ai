import Foundation
import Vision
import CoreImage
import AppKit

// personmask <out_dir> <in1.png> [in2.png ...]
// Writes <out_dir>/<basename>.mask.png — 8-bit grayscale person mask, same size as input.

let args = CommandLine.arguments
guard args.count >= 3 else { FileHandle.standardError.write("usage: personmask OUTDIR IN...\n".data(using:.utf8)!); exit(2) }
let outDir = args[1]
try? FileManager.default.createDirectory(atPath: outDir, withIntermediateDirectories: true)
let ctx = CIContext(options: [.useSoftwareRenderer: false])

for path in args[2...] {
    guard let src = CIImage(contentsOf: URL(fileURLWithPath: path)) else {
        print("ERR\t\(path)\tload"); continue
    }
    let req = VNGeneratePersonSegmentationRequest()
    req.qualityLevel = .accurate
    req.outputPixelFormat = kCVPixelFormatType_OneComponent8
    let handler = VNImageRequestHandler(ciImage: src, options: [:])
    do { try handler.perform([req]) } catch { print("ERR\t\(path)\t\(error)"); continue }
    guard let obs = req.results?.first else { print("ERR\t\(path)\tnoresult"); continue }
    var mask = CIImage(cvPixelBuffer: obs.pixelBuffer)
    // Vision returns the mask at its own resolution; scale to the source extent.
    let se = src.extent, me = mask.extent
    mask = mask.transformed(by: CGAffineTransform(scaleX: se.width/me.width, y: se.height/me.height))
    let name = (path as NSString).lastPathComponent
    let base = (name as NSString).deletingPathExtension
    let outURL = URL(fileURLWithPath: "\(outDir)/\(base).mask.png")
    let cs = CGColorSpaceCreateDeviceGray()
    do {
        try ctx.writePNGRepresentation(of: mask, to: outURL, format: .L8, colorSpace: cs)
        print("OK\t\(path)")
    } catch { print("ERR\t\(path)\twrite \(error)") }
}
