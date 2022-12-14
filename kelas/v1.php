<?php
namespace GroupA;
require '../vendor/autoload.php';
use GroupA\v5;
use GroupA\v7;
use Carbon\Carbon;
class v1 {
    public function cetakUmur($input) {
        $objek_v7 = new v7();
        $umur = $objek_v7->formatDesimal($input);
        $objek_v5 = new v5();
        $objek_v5->cetakAngka($umur);
    }
    public function cetakTanggalSekarang() {
        $date = Carbon::now()->toDateString();
        echo $date;
    }
}