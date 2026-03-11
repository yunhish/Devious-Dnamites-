<?php
require "db.php";

if(isset($_GET["token"])){

$token = $_GET["token"];

$stmt = $conn->prepare("
SELECT id, token_expiry 
FROM users 
WHERE verification_token=? LIMIT 1
");

$stmt->bind_param("s",$token);
$stmt->execute();

$result = $stmt->get_result();

if($result->num_rows > 0){

$user = $result->fetch_assoc();

if(strtotime($user["token_expiry"]) > time()){

$update = $conn->prepare("
UPDATE users 
SET is_verified=1, verification_token=NULL 
WHERE id=?
");

$update->bind_param("i",$user["id"]);
$update->execute();

echo "Email verified successfully.";

}
else{
echo "Verification link expired.";
}

}
else{
echo "Invalid token.";
}

}
?>
