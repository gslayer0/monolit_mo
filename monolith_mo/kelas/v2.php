<?php

namespace GroupA;
use GroupA\v4;
use GroupA\v5;
class v2 {
    public function cetakBulanKelahiran($bulan) {
        $objek_v4 = new v4();
        $objek_v4->cetakKalimat($bulan);
    }
    public function cetakTanggalKelahiran($tanggal) {
        $objek_v5 = new v5();
        $objek_v5->cetakAngka( $tanggal);
    }
}