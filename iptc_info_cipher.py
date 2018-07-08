from iptcinfo import IPTCInfo
import fire

class IPTCInfoCipher:
    """
    Provides utilities to set and get lists into the IPTC special_instructions field of a .JPG file.
    Note: the 2018 Adobe tools show this as the Instructions field of the IPTC core set of data

    To see more detailed help run IPTCInfoTools <command> --help
    """
    def __init__(self):
        self._password = b"31EAC3A1F3079064"  #default password used for testing
        self._salt = b"16321B5A750850C7"      #application specific salt for mixing with password

    def print_iptcinfo(self,filename):
        """
        Prints the IPC Info for the specified filename
        :param filename: .jpg filename
        :return: none
        """
        info = IPTCInfo(filename)
        if len(info.data) < 4: raise Exception(info.error)

        # Print list of keywords, supplemental categories, contacts
        print("Keywords:{}".format(info.keywords))
        print("SupplementalCatagories:{}".format(info.supplementalCategories))
        print("Contacts:{}".format(info.contacts))
        print("Data:{}".format(info.data))

        tags = ['date created', 'digital creation date', 'reference number', 'custom8', 'custom9', 'sub-location',
                'object cycle', 'custom4', 'custom5', 'custom6', 'custom7', 'custom1', 'custom2', 'reference date',
                'by-line title', 'local caption', 'keywords', 'province/state', 'category', 'custom17', 'custom14',
                'digital creation time', 'custom12', 'custom13', 'custom10', 'custom11', 'headline', 'custom18',
                'custom19', 'source', 'contact', 'by-line', 'object name', 'content location code',
                'language identifier', 'release date', 'expiration date', 'reference service', 'custom16',
                'original transmission reference', 'originating program', 'subject reference', 'city',
                'supplemental category', 'content location name', 'country/primary location code', 'editorial update',
                'custom15', 'fixture identifier', 'custom3', 'country/primary location name', 'action advised',
                'custom20', 'copyright notice', 'program version', 'image orientation', 'edit status',
                'expiration time', 'release time', 'credit', 'time created', 'special instructions', 'writer/editor',
                'caption/abstract', 'urgency', 'image type']

        for i in tags:
            desc=info.data[i]
            print("  {0}:{1}".format(i,desc))


    def read_list_from_jpg(self, filename):
        """
        Reads a list of data from the IPTC special_instructions field of a .JPG file
        :param filename: .jpg filename
        :return: list of items
        """
        info = IPTCInfo(filename)
        if len(info.data) < 4: raise Exception(info.error)
        s = info.data['special instructions']
        items = eval(s)
        return items

    def read_encrypted_list_from_jpg(self, filename, password):
        """
        Reads a list of data encrypted in the IPTC special_instructions field of a .JPG file
        :param filename: .jpg filename
        :param  password: the password used for encryption
        :return: list of items
        """
        self._password=password
        info = IPTCInfo(filename)
        if len(info.data) < 4: raise Exception(info.error)
        token = info.data['special instructions']
        s = self._fermet_decrypt(token)
        items = eval(s)
        return items

    def write_list_to_jpg(self, filename, items):
        """
        Writes a list of data to the IPTC special_instructions field of a .JPG file
        :param filename: .jpg filename
        :param items: list of items to be written (specified using Python list syntax)
        :return: none
        """
        info = IPTCInfo(filename)
        if len(info.data) < 4: raise Exception(info.error)
        info.data['caption/abstract']='Contains Special Instructions'
        info.data['special instructions']=str(items)
        info.save()

    def write_encrypted_list_to_jpg(self, filename, password, items):
        """
        Writes an encrypted list of data to the IPTC special_instructions field of a .JPG file
        :param filename: .jpg filename
        :param password: the password used for encryption
        :param items: list of items to be written (specified using Python list syntax)
        :return: none
        """
        self._password=password
        info = IPTCInfo(filename)
        if len(info.data) < 4: raise Exception(info.error)
        token = self._fernet_encrypt(str(items))
        info.data['caption/abstract']='Contains Special Instructions'
        info.data['special instructions']=token
        info.save()

    def _fernet_encrypt(self, s):
        import base64
        import os
        from cryptography.fernet import Fernet
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

        kdf = PBKDF2HMAC(
            algorithm = hashes.SHA256(),
            length = 32,
            salt = self._salt,
            iterations = 100000,
            backend = default_backend()
        )

        key = base64.urlsafe_b64encode(kdf.derive(self._password))
        f = Fernet(key)
        token = f.encrypt(s)
        s1 = f.decrypt(token)
        assert(s==s1)
        return token

    def  _fermet_decrypt(self, token):
        import base64
        import os
        from cryptography.fernet import Fernet
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC



        kdf = PBKDF2HMAC(
            algorithm = hashes.SHA256(),
            length = 32,
            salt = self._salt,
            iterations = 100000,
            backend = default_backend()
        )

        key = base64.urlsafe_b64encode(kdf.derive(self._password))
        f = Fernet(key)
        s = f.decrypt(token)
        return s


if __name__ == '__main__':
    fire.Fire(IPTCInfoCipher)


