// Apple Vision face pose for kit9x16/auto_content.py. Free, on-device.
// usage: vision_face <image> [<image> ...] -> one JSON object per line:
//   {"image": path, "faces": [{"yaw": deg, "roll": deg, "box": [x0, y0, x1, y1]}]}   (largest face first)
import Foundation
import Vision
import AppKit

for path in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        print("{\"image\": \"\(path)\", \"faces\": []}")
        continue
    }
    let W = Double(cg.width), H = Double(cg.height)
    let req = VNDetectFaceRectanglesRequest()
    let h = VNImageRequestHandler(cgImage: cg, options: [:])
    try? h.perform([req])
    let faces = (req.results ?? []).sorted { $0.boundingBox.width * $0.boundingBox.height > $1.boundingBox.width * $1.boundingBox.height }
    var parts: [String] = []
    for f in faces {
        let b = f.boundingBox
        let yaw = (f.yaw?.doubleValue ?? 0) * 180 / Double.pi
        let roll = (f.roll?.doubleValue ?? 0) * 180 / Double.pi
        parts.append(String(format: "{\"yaw\": %.1f, \"roll\": %.1f, \"box\": [%.1f, %.1f, %.1f, %.1f]}",
                            yaw, roll, b.minX * W, (1 - b.maxY) * H, b.maxX * W, (1 - b.minY) * H))
    }
    print("{\"image\": \"\(path)\", \"faces\": [\(parts.joined(separator: ", "))]}")
}
