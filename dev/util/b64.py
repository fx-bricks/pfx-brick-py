import base64

data = open("pink3dB.wav", "rb").read()
encoded = base64.b64encode(data)
print("Data size %d" % (len(data)))
print("Encoded size %d" % (len(encoded)))
with open("yb64.txt", "wb") as f:
    f.write(encoded)
