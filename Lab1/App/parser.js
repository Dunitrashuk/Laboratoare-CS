let fileName;
let auditFile;
let parsedAudit = {};

function run() {
    auditFile = document.getElementById("audit-file").files[0];
    fileName = document.getElementById("save-location").value;

    parseAudit(auditFile);
    saveAudit();
    alert("Parsed Audit JSON Saved");
}

function saveAudit() {
    let data = encode( JSON.stringify(parsedAudit, null, 4) );
    let blob = new Blob( [ data ], {
        type: 'application/octet-stream'
    });

    let url = URL.createObjectURL( blob );
    let link = document.createElement( 'a' );
    link.setAttribute( 'href', url );
    link.setAttribute( 'download', fileName );

    let event = document.createEvent( 'MouseEvents' );
    event.initMouseEvent( 'click', true, true, window, 1, 0, 0, 0, 0, false, false, false, false, 0, null);
    link.dispatchEvent( event );
}

function parseAudit(file) {
    let reader = new FileReader();
    let item;
    reader.onload = function(){
        let lines = this.result.split('\n');
        let j = 0;
        for(let i = 0; i < lines.length; i++){
            if(lines[i].includes("<custom_item>")){
                item = {};
                while (!(lines[i+1].includes("</custom_item>"))) {
                    item[lines[i+1].substring(0, lines[i+1].indexOf(":"))] = lines[i+1].substring(lines[i+1].indexOf(":") + 1);
                    i++;
                }
                parsedAudit[j] = item;
                j++;
            }
        }
        console.log(parsedAudit);
    };
    reader.readAsText(file);
}

function encode( s ) {
    let out = [];
    for (let i = 0; i < s.length; i++ ) {
        out[i] = s.charCodeAt(i);
    }
    return new Uint8Array( out );
}

