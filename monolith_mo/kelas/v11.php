<?php
namespace GroupB;
use GroupB\v8;
class v11 {
    public function cetakKalimatBesar(string $input) {
        $kalimat = (string) $input;
        $kalimat = strtoupper($kalimat);
        $objek_v8 = new v8();
        $objek_v8->cetak($kalimat);
    }
}