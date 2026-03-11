<?php
require "db.php";

$email = $_POST["email"];
$password = $_POST["password"];

$stmt = $conn->prepare("
SELECT password,is_verified 
FROM users 
WHERE email=?
");

$stmt->bind_param("s",$email);
$stmt->execute();

$result = $stmt->get_result();

if($result->num_rows > 0){

$user = $result->fetch_assoc();

if(password_verify($password,$user["password"])){

if($user["is_verified"] == 1){

echo "Login successful";

}else{

echo "Please verify your email first.";

}

}else{

echo "Incorrect password";

}

}else{

echo "User not found";

}
?>
