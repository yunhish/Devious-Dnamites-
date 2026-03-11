<?php
require "db.php";

if($_SERVER["REQUEST_METHOD"] == "POST"){

$name = $_POST["name"];
$email = $_POST["email"];
$password = password_hash($_POST["password"], PASSWORD_DEFAULT);
$department_id = $_POST["department_id"];

$token = bin2hex(random_bytes(32));
$expiry = date("Y-m-d H:i:s", strtotime("+1 hour"));

$stmt = $conn->prepare("
INSERT INTO users 
(name,email,password,department_id,verification_token,token_expiry)
VALUES (?,?,?,?,?,?)
");

$stmt->bind_param(
"sssiss",
$name,
$email,
$password,
$department_id,
$token,
$expiry
);

if($stmt->execute()){

$verify_link = "https://yourdomain.com/verify.php?token=".$token;

$subject = "Verify Your Student Account";

$message = "
Hello $name,

Please verify your student account:

$verify_link

This link expires in 1 hour.
";

$headers = "From: noreply@yourdomain.com";

mail($email,$subject,$message,$headers);

echo "Registration successful. Check your email to verify.";

}
else{
echo "Registration failed.";
}

}
?>
