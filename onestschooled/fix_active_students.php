<?php
$pdo = new PDO('mysql:host=localhost;dbname=onest_school', 'root', '');
$pdo->exec("UPDATE counter_translates SET total_count = '4' WHERE name = 'Active Students'");
echo "✅ Active Students counter fixed to 4\n";
