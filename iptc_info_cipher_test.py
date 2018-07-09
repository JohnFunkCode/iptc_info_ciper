import unittest
import iptc_info_cipher

class test_iptc_info_cipher(unittest.TestCase):

    def setUp(self):
        return

    def test_encrypt_decrypt(self):
        aIC = iptc_info_cipher.IPTCInfoCipher()
        input_string="Hello World"
        token=aIC._fernet_encrypt(input_string,"password")
        output_string=aIC._fermet_decrypt(token,"password")
        self.assertTrue(input_string==output_string)

    def test_print_iptcinfo(self):
        aIC = iptc_info_cipher.IPTCInfoCipher()
        aIC.print_iptcinfo("Clippy.jpg")

    def test_write_and_read_from_jpg(self):
        aIC = iptc_info_cipher.IPTCInfoCipher()
        input_list=[1,2,3,4,5]
        aIC.write_list_to_jpg("Clippy.jpg",input_list)
        output_list=aIC.read_list_from_jpg("Clippy.jpg")
        self.assertTrue(set(input_list).intersection(output_list))

    def test_encrypted_write_and_read_from_jpg(self):
        aIC = iptc_info_cipher.IPTCInfoCipher()
        input_list=[1,2,3,4,5]
        aIC.write_encrypted_list_to_jpg("ClippyCrypto.jpg","password",input_list)
        output_list=aIC.read_encrypted_list_from_jpg("ClippyCrypto.jpg","password")
        self.assertTrue(set(input_list).intersection(output_list))

    def test_read_list_from_url(self):
        aIC = iptc_info_cipher.IPTCInfoCipher()
        url = "https://github.com/JohnFunkCode/iptc_info_ciper/raw/master/Clippy.jpg"
        l=aIC.read_list_from_url(url)
        #print("data from {}:{}".format(url,l))
        self.assertTrue(len(l)>0)

    def test_read_encrypted_list_from_url(self):
        aIC = iptc_info_cipher.IPTCInfoCipher()
        url = "https://github.com/JohnFunkCode/iptc_info_ciper/raw/master/ClippyCrypto.jpg"
        l=aIC.read_encrypted_list_from_url(url,"password")
        #print("data from encrypted {}:{}".format(url,l))
        self.assertTrue(len(l)>0)


if __name__ == '__main__':
    unittest.main()