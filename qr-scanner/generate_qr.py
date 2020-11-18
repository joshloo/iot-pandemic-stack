import qrcode

code = qrcode.make('Loo Tung Lun;010101-02-0303')
code.save('tunglun_qr.png')