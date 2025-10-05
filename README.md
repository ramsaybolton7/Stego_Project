# 🕵️‍♂️ Steganography using LSB (Least Significant Bit) in Python

This project demonstrates how to hide secret text messages inside images using **Least Significant Bit (LSB) steganography** — a simple and effective data-hiding technique in the field of **Computer Security**.

---

## 🧠 Overview

**Steganography** is the art of hiding information within other non-secret data.  
In this project, a text message is embedded into the **least significant bits of pixel values** in an image, so that:
- The visual quality of the image remains unchanged.
- The message can later be extracted (decoded) perfectly.

This project was developed as part of a **Computer Security course assignment**.

---

## 🔐 Features

- Hides secret text messages inside image files (PNG format).  
- Extracts hidden messages from stego images.  
- No visible change in the image after encoding.  
- Works entirely offline, written in **pure Python**.  
- Easy to customize for learning or experimentation.

---

## ⚙️ Tech Stack

| Component | Description |
|------------|-------------|
| **Language** | Python 3.x |
| **Library** | Pillow (for image processing) |
| **IDE** | Visual Studio Code |
| **Image Format** | PNG (lossless) |

---

## 🧩 How It Works

### 1️⃣ Encoding (Hiding the Message)
1. Convert secret text → binary bits.  
2. Store the message length in the first 32 bits of the image.  
3. Replace each pixel’s RGB least significant bit with the message bits.  
4. Save the modified image as a **stego image**.

### 2️⃣ Decoding (Retrieving the Message)
1. Read the LSBs of each pixel.  
2. Extract the first 32 bits to determine message length.  
3. Read next *n* bits as message data.  
4. Convert binary → text → print message.

---

## 🧮 Example Output

**Input Image:**  
`sample_image.png`  

**Secret Message:**  
