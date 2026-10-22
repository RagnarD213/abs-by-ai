// personmask IN.png OUT_MASK.png  -> writes a full-size person mask (Apple Vision, accurate) and prints face boxes as JSON
// (pixel coords, top-left origin). Used by qc.py to keep cover type clear of the person, face and hair.
import Foundation
import Vision
import CoreImage
import AppKit
let a=CommandLine.arguments
guard a.count==3, let src=CIImage(contentsOf: URL(fileURLWithPath:a[1])) else { print("usage: personmask IN OUT"); exit(2) }
let W=src.extent.width, H=src.extent.height
let h=VNImageRequestHandler(ciImage: src)
let seg=VNGeneratePersonSegmentationRequest(); seg.qualityLevel = .accurate; seg.outputPixelFormat = kCVPixelFormatType_OneComponent8
let face=VNDetectFaceRectanglesRequest()
try h.perform([seg, face])
var boxes:[[Int]]=[]
for f in face.results ?? [] { let b=f.boundingBox; boxes.append([Int(b.minX*W), Int((1-b.maxY)*H), Int(b.maxX*W), Int((1-b.minY)*H)]) }
if let m=seg.results?.first?.pixelBuffer {
  var ci=CIImage(cvPixelBuffer:m); ci=ci.transformed(by: CGAffineTransform(scaleX: W/ci.extent.width, y: H/ci.extent.height))
  let ctx=CIContext(); let cs=CGColorSpaceCreateDeviceGray()
  try ctx.writePNGRepresentation(of: ci, to: URL(fileURLWithPath:a[2]), format: .L8, colorSpace: cs)
}
print("{\"faces\":\(boxes)}")
