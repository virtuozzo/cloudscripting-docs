<?php
    $token = "2226f9ddd3bd1f430afb99be023646a889f1a52e";
    $url = "https://api.github.com/repos/dzotic9/docs/issues";
    $selectedText = $_GET['selected'];
    $userName = $_GET['userName'];
    $position = $_GET['topPosition'];
    $comment = $_GET['comment'];
    $labels = "cs-bug-report";
    $page = $_GET['page'];
    $assignee = "dzotic9";
    $title = "CS-issue";

    $text = "Target page: " .$page.
        "<br>Name: " .$userName.
        "<br>Selected text: " .$selectedText.
        "<br>Comment: " .$comment.
        "<br>Position: " .$position;

    $text = str_replace("\n","\\n",$text);
    $data = '{"title": "'. $title .'", "body": "'. addslashes($text) .'", "assignee": "'. $assignee .'", "labels": ["'. $labels .'"]}';

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        'User-Agent: PHP',
        'Authorization: token '.$token
    ));
    $server_output = curl_exec($ch);
    curl_close ($ch);
    print_r($server_output)
?>