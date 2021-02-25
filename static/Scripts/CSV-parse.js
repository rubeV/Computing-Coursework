$.ajax({
  url: '/static/Data/POP.csv',
  dataType: 'text',
}).done(makeTable);

function makeTable ( csv ) {

    var rows = csv.split('\n'),
    table = document.getElementById('main-table'),
    tr = null, td = null,
    tds = null;
    var trcss = null;
    trcss = document.createElement('tbody');
    for ( var i = 0; i < rows.length; i++ ) {
        tr = document.createElement('tr');
        tds = rows[i].split(',');
        for ( var j = 0; j < tds.length; j++ ) {
           td = document.createElement('td');
           td.innerHTML = tds[j];
           tr.appendChild(td);
        }
        trcss.appendChild(tr);
    }
    table.appendChild(trcss);
    document.body.appendChild(table);

}

