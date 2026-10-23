// Person boxes per image (Vision human rectangles). Usage: swift people.swift <dir-of-pngs> > boxes.txt
// Prints: filename x y w h [x y w h ...] (normalised, origin top-left). Feed it to trackcrop.py.
import Foundation
import Vision
import AppKit
let dir = CommandLine.arguments[1]
let files = try FileManager.default.contentsOfDirectory(atPath: dir).filter { $0.hasSuffix(".png") }.sorted()
for f in files {
    guard let img = NSImage(contentsOfFile: dir + "/" + f), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { print(f); continue }
    let req = VNDetectHumanRectanglesRequest()
    req.upperBodyOnly = false
    try? VNImageRequestHandler(cgImage: cg).perform([req])
    var out = f
    for o in req.results ?? [] {
        let b = o.boundingBox
        out += String(format: " %.4f %.4f %.4f %.4f", b.minX, 1 - b.maxY, b.width, b.height)
    }
    print(out)
}
