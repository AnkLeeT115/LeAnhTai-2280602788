import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Ensure txt_info is editable
        self.ui.txt_info.setReadOnly(False)  # Allow user input in txt_info
        
        # Connect buttons to their respective functions
        self.ui.btn_gen.clicked.connect(self.call_api_generate_keys)
        self.ui.btn_enc.clicked.connect(self.call_api_encrypt)
        self.ui.btn_dec.clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    def call_api_generate_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_info.setText(data["message"])
                QMessageBox.information(self, "Success", "Keys Generated Successfully")
            else:
                self.ui.txt_info.setText("Error generating keys")
                print("Error while calling generate keys API")
        except requests.exceptions.RequestException as e:
            self.ui.txt_info.setText(f"Error: {str(e)}")
            print(f"Error: {str(e)}")

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        payload = {
            "message": self.ui.txt_plt.toPlainText(),
            "key_type": "public"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cpt.setText(data["encrypted_message"])
                self.ui.txt_info.setText("Encryption Successful")
                QMessageBox.information(self, "Success", "Encrypted Successfully")
            else:
                self.ui.txt_info.setText("Error during encryption")
                print("Error while calling encrypt API")
        except requests.exceptions.RequestException as e:
            self.ui.txt_info.setText(f"Error: {str(e)}")
            print(f"Error: {str(e)}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"
        payload = {
            "ciphertext": self.ui.txt_cpt.toPlainText(),
            "key_type": "private"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                decrypted_message = data["decrypted_message"]
                if decrypted_message:
                    self.ui.txt_plt.setText(decrypted_message)
                    self.ui.txt_info.setText("Decryption Successful")
                    QMessageBox.information(self, "Success", "Decrypted Successfully")
                else:
                    self.ui.txt_info.setText("Decryption Failed: Invalid ciphertext or key")
                    QMessageBox.warning(self, "Warning", "Decryption Failed")
            else:
                self.ui.txt_info.setText("Error during decryption")
                print("Error while calling decrypt API")
        except requests.exceptions.RequestException as e:
            self.ui.txt_info.setText(f"Error: {str(e)}")
            print(f"Error: {str(e)}")

    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"
        payload = {
            "message": self.ui.txt_plt.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_sign.setText(data["signature"])
                self.ui.txt_info.setText("Signature Generated")
                QMessageBox.information(self, "Success", "Signed Successfully")
            else:
                self.ui.txt_info.setText("Error during signing")
                print("Error while calling sign API")
        except requests.exceptions.RequestException as e:
            self.ui.txt_info.setText(f"Error: {str(e)}")
            print(f"Error: {str(e)}")

    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"
        payload = {
            "message": self.ui.txt_plt.toPlainText(),
            "signature": self.ui.txt_sign.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if data["is_verified"]:
                    self.ui.txt_info.setText("Signature Verified Successfully")
                    QMessageBox.information(self, "Success", "Signature Verified")
                else:
                    self.ui.txt_info.setText("Signature Verification Failed")
                    QMessageBox.warning(self, "Warning", "Signature Verification Failed")
            else:
                self.ui.txt_info.setText("Error during verification")
                print("Error while calling verify API")
        except requests.exceptions.RequestException as e:
            self.ui.txt_info.setText(f"Error: {str(e)}")
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())