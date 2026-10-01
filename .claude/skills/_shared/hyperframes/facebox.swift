import Foundation
import Vision
import CoreImage

// facebox <in1.png> [in2.png ...]
// Prints one line per image: <path>\t<x0> <y0> <x1> <y1> (pixels, top-left origin) for the largest face, or <path>\tnone.
// Used by hyperframes/checks.py to prove a lower third never covers Dan's face.
for path in CommandLine.arguments.dropFirst() {
    guard let src = CIImage(contentsOf: URL(fileURLWithPath: path)) else { print("\(path)\terror"); continue }
    let req = VNDetectFaceRectanglesRequest()
    let handler = VNImageRequestHandler(ciImage: src, options: [:])
    do { try handler.perform([req]) } catch { print("\(path)\terror"); continue }
    let w = src.extent.width, h = src.extent.height
    let faces = (req.results ?? []).sorted { $0.boundingBox.width * $0.boundingBox.height > $1.boundingBox.width * $1.boundingBox.height }
    guard let f = faces.first else { print("\(path)\tnone"); continue }
    let b = f.boundingBox
    let x0 = Int(b.minX * w), x1 = Int(b.maxX * w), y0 = Int((1 - b.maxY) * h), y1 = Int((1 - b.minY) * h)
    print("\(path)\t\(x0) \(y0) \(x1) \(y1)")
}
