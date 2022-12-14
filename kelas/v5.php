<?php

namespace GroupA;
use v6;
use GroupA\v7;
class v5 {
    public function cetakAngka($input) {
        $angka = (int) $input;
        $kelas_v7 = new v7();
        $angka = $kelas_v7->formatDesimal($angka);
        $kelas_v6 = new v6();
        $kelas_v6->printInput($angka);
    }
}