<?php
namespace GroupA;
use GroupA\v4;
class v3 {
    public function cetakNamaPanjang(string $nama_lengkap) {
        $objek_v4 = new v4();
        $objek_v4->cetakKalimat($nama_lengkap);
    }
}