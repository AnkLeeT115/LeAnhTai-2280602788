from flask import Flask, render_template, request
from cipher.caesar import CaesarCipher


app = Flask(__name__)


# Route for home page
@app.route("/")
def home():
    return render_template('index.html')


# Route for caesar cipher page
@app.route("/caesar")
def caesar():
    return render_template('caesar.html')
@app.route("/vigenere")
def vigenere():
    return render_template('Vigenere.html')
@app.route("/railfence")
def railfence():
    return render_template('railfence.html')
@app.route("/Transposition")
def transposition():
    return render_template('transposition.html')
@app.route("/playfair")
def playfair():
    return render_template('playfair.html')



# Route for Caesar encryption
@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    caesar = CaesarCipher()  # Corrected instance creation
    encrypted_text = caesar.encrypt_text(text, key)
    return f"Text: {text}<br/>Key: {key}<br/>Encrypted text: {encrypted_text}"


# Route for Caesar decryption
@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    caesar = CaesarCipher()  # Corrected instance creation
    decrypted_text = caesar.decrypt_text(text, key)
    return f"Text: {text}<br/>Key: {key}<br/>Decrypted text: {decrypted_text}"


# Main function to run the app
if __name__ == '__main__':  # Fixed if condition
    app.run(host="0.0.0.0", port=5050, debug=True)

