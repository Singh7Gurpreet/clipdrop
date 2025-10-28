
# Clipdrop Android and macOS

## Motivation:
I needed something very similar to AirDrop like for Android to macOS. One of my friends has a very long conversation data in WhatsApp. If I send him something over WhatsApp and want to load it to his own personal computer. He needed to load WhatsApp web, which always takes a lot of time, like from 1-2 minutes, just for getting a file to his laptop. He could use Drive, which would lead to wastage of storage, and the other one is emailing himself, but it does not work for larger files. So, I tried to mimic Apple’s ecosystem technology for Android to macOS. In this application, one can simply share a file through his Android phone through my app, and it is available on macOS to be copied anywhere. I will be starting with clipboard content, which I personally use a lot from macOS to iPhone or vice versa.

## Technologies Used:

HTTP Server: Node.js, deployed on Render service.
Background Daemon for macOS: Python
Android application: Java
Cloud Storage Service: AWS S3 (single bucket only)
Authentication: Google OAuth
Local Communication: Bluetooth Low Energy(added in 2nd iteration of application).

## Documented Learning/ Brain Dump:

My https server simply supports simple operations such as GET, POST, and PUT; most of the endpoints are just wrappers for my Amazon S3. This was much needed because I do not want to waste network resources such that my server handles download and upload. It is resolved by the use of pre-signed URLs supported by S3. A background daemon in macOS listens for changes in the clipboard. If the copied content is simple text, it simply uploads it to the server as text.txt. It first fetches the pre-signed URL from my server, which is then used to upload that file. The metadata is stored as follows: Hashed(JWT_TOKEN)__DELIMIT__Clipboard__DELIMIT__filename.ext for clipboard files; for storage-related files, we replace Clipboard by Storage. So that fetching becomes easier and it is easy to handle if the user simply copies text.txt as a file which could not be our clipboard content. When uploading is done, it simply sends a Bluetooth event clipboard to Android, which gets to know clipboard content is available to download. Then it simply requests a download link from my https server, which requests files using this as a prefix search Hashed(JWT_TOKEN), which gives us all files that are related to that user; why all this prefix search? It allows me not to use any kind of Redis-like database to keep association of users and their files. After getting the link to the clipboard file, it downloads, reads, and then pastes into its own clipboard. This is how it gave a backbone for sharing storage content; now all we have to do is replace clipboard with storage in our endpoints API and metadata of Amazon S3. Let’s start from Android: a user took a photo now wants to save to his personal computer. The user shares that photo; let’s assume it’s a JPEG file. Now the Android app requests a pre-signed URL for uploading that file from the https server. After it gets that link, it uploads that file using this metadata in S3 as Hashed(JWT_TOKEN)__DELIMIT__Storage__DELIMIT__filename.jpeg. After uploading it, it simply emits a Bluetooth event storage to a personal computer, which then follows the same steps as in clipboard content fetching. But some extra steps for saving that to the clipboard are required. In macOS, we have osxscript, which can be used to manipulate the clipboard for storing file content, so I used it for saving it to my clipboard. But in Ubuntu, we do not have any; it can be saved at the user’s required location, which could be Desktop or Download. And in Windows, we have one but have not used it for Windows.

This is everything about my project, although this is not production grade. I have made it for personal use only.
