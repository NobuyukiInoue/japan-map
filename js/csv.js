//CSVファイルを読み込む関数getCSV()の定義
function getCSV(url_csvfile, element_result, element_table){
    var req = new XMLHttpRequest();      // HTTPでファイルを読み込むためのXMLHttpRrequestオブジェクトを生成
    req.open("get", url_csvfile, true);  // アクセスするファイルを指定
    req.send(null);                      // HTTPリクエストの発行

    // レスポンスが返ってきたらconvertCSVtoArray()を呼ぶ
    req.onload = function() {
        var csv_data = convertCSVtoArray(req.responseText);
        element_result.val = csv_data;

        var insertHTML = createTable(csv_data, "myTable", "tablesorter", "line-height:1.4em; font-size:95%;", "1");
        element_table.appendChild(insertHTML);
    }
}

// 読み込んだCSVデータを二次元配列に変換する
function convertCSVtoArray(str) {        // 読み込んだCSVデータが文字列として渡される
    var result = [];                     // 最終的な二次元配列を入れるための配列
    var tmp = str.split("\n");           // 改行を区切り文字として行を要素とした配列を生成
 
    // 各行ごとにカンマで区切った文字列を要素とした二次元配列を生成
    for(var i=0;i<tmp.length;++i) {
        result[i] = tmp[i].split(',');
    }

    return result;
}

// tableタグを出力する
function createTable(data, arg_id, arg_class, arg_style, arg_border) {
    var table = document.createElement('table');
    table.setAttribute("id", arg_id);
    table.setAttribute("class", arg_class);
    table.setAttribute("style", arg_style);
    table.setAttribute("border", arg_border);

    var tbody = document.createElement('tbody');
    for (var i = 0; i < data.length; i++) {
        var tr = document.createElement('tr');
        for (var j = 0; j < data[i].length; j++) {
            var td = document.createElement('td');
            if (j == 1) {
               td.innerText = data[i][j].substring(2);
            } else if (i > 0 && 6 <= j && j <= 8 ){
                td.innerText = Number(data[i][j]).toLocaleString();
                td.setAttribute("align", "right");
            } else {
               td.innerText = data[i][j];
            }
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    }

    table.appendChild(tbody);
    return table;
}

// 都道府県名を探し、レコード番号を返す
function get_record(csv_data, target_name) {
    for (var i = 0; i < csv_data.length; i++) {
        if (csv_data[i][1].indexOf(target_name) >= 0) {
            return i;
        }
    }
}
