// Detect the largest face in each image. Usage: swift faces.swift <dir-of-pngs>
// Prints: filename x y w h (normalised, origin top-left) or "none".
import Foundation
import Vision
import AppKit

let dir = CommandLine.arguments[1]
let files = try FileManager.default.contentsOfDirectory(atPath: dir).filter { $0.hasSuffix(".png") }.sorted()
for f in files {
    guard let img = NSImage(contentsOfFile: dir + "/" + f),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { print(f, "none"); continue }
    let req = VNDetectFaceRectanglesRequest()
    try VNImageRequestHandler(cgImage: cg).perform([req])
    let faces = (req.results ?? []).sorted { $0.boundingBox.width > $1.boundingBox.width }
    if let b = faces.first?.boundingBox {
        print(f, String(format: "%.3f %.3f %.3f %.3f", b.minX, 1 - b.maxY, b.width, b.height))
    } else { print(f, "none") }
}
