import AppKit
import CryptoKit
import Security
import Foundation

// No browser cookies or publishing key. The new private key lives in Keychain.
let service="com.absbyai.wallpaper-reader.v1"
let account="favorites-only"
func fail(_ message:String) -> Never { FileHandle.standardError.write(Data((message+"\n").utf8)); exit(1) }
func output(_ object:Any) throws { print(String(data:try JSONSerialization.data(withJSONObject:object,options:[.sortedKeys]),encoding:.utf8)!) }
func key(create:Bool=false) throws -> Curve25519.Signing.PrivateKey {
 let query:[String:Any]=[kSecClass as String:kSecClassGenericPassword,kSecAttrService as String:service,kSecAttrAccount as String:account]
 var item:CFTypeRef?
 let status=SecItemCopyMatching(query.merging([kSecReturnData as String:true,kSecMatchLimit as String:kSecMatchLimitOne]){_,b in b} as CFDictionary,&item)
 if status==errSecSuccess,let data=item as? Data { return try Curve25519.Signing.PrivateKey(rawRepresentation:data) }
 guard create && status==errSecItemNotFound else { fail("Wallpaper reader key unavailable. Enrollment requires explicit approval.") }
 let key=Curve25519.Signing.PrivateKey()
 let attributes=query.merging([kSecValueData as String:key.rawRepresentation,kSecAttrAccessible as String:kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly]){_,b in b}
 guard SecItemAdd(attributes as CFDictionary,nil)==errSecSuccess else { fail("Keychain enrollment failed") }
 return key
}
func publicDER(_ key:Curve25519.Signing.PrivateKey)->Data {
 // RFC 8410 Ed25519 SubjectPublicKeyInfo prefix, followed by 32 public bytes.
 return Data([0x30,0x2a,0x30,0x05,0x06,0x03,0x2b,0x65,0x70,0x03,0x21,0x00])+key.publicKey.rawRepresentation
}
func screenID(_ screen:NSScreen)->String { String((screen.deviceDescription[NSDeviceDescriptionKey("NSScreenNumber")] as? UInt32) ?? 0) }
func screens()->[[String:Any]] {
 NSScreen.screens.map{["id":screenID($0),"name":$0.localizedName,"path":NSWorkspace.shared.desktopImageURL(for:$0)?.path ?? ""]}
}
do {
 guard CommandLine.arguments.count==2 else { fail("Choose --inspect, --apply, --sign, --public, or --enroll") }
 switch CommandLine.arguments[1] {
 case "--inspect":try output(screens())
 case "--enroll":try output(["publicKey":publicDER(try key(create:true)).base64EncodedString()])
 case "--public":try output(["publicKey":publicDER(try key()).base64EncodedString()])
 case "--sign":
  let input=FileHandle.standardInput.readDataToEndOfFile()
  guard input.count<16384 else { fail("Signing input too large") }
  let key=try key();let der=publicDER(key)
  try output(["signature":try key.signature(for:input).base64EncodedString(),"keyId":SHA256.hash(data:der).map{String(format:"%02x",$0)}.joined()])
 case "--apply":
  let input=FileHandle.standardInput.readDataToEndOfFile()
  guard input.count<16384,let entries=try JSONSerialization.jsonObject(with:input) as? [[String:String]],entries.count<=3 else { fail("Invalid wallpaper plan") }
  for entry in entries {
   guard let id=entry["id"],let path=entry["path"],let screen=NSScreen.screens.first(where:{screenID($0)==id}),FileManager.default.fileExists(atPath:path) else { fail("Display or original image unavailable") }
   let url=URL(fileURLWithPath:path)
   try NSWorkspace.shared.setDesktopImageURL(url,for:screen,options:[.imageScaling:NSImageScaling.scaleProportionallyUpOrDown.rawValue,.allowClipping:true])
  }
  let observed=screens()
  for entry in entries { guard observed.contains(where:{$0["id"] as? String==entry["id"] && $0["path"] as? String==entry["path"]}) else { fail("Mac wallpaper readback did not match") } }
  try output(observed)
 default:fail("Unknown action")
 }
} catch { fail("Wallpaper helper failed: \(error.localizedDescription)") }
