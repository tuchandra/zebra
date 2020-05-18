function logic_clear() {
    for(var a=0;a<logic_attrs;a++) {
        for(var i=0;i<logic_size;i++) {
            for(var h=0;h<logic_size;h++) {
                document.getElementById("B"+a+i+h).checked=false;
                document.getElementById("C"+a+i+h).style.backgroundColor='white';
            }
        }
    }
}
function logic_set() {
    for(var a=0;a<logic_attrs;a++) {
        for(var i=0;i<logic_size;i++) {
            for(var h=0;h<logic_size;h++) {
                document.getElementById("B"+a+i+h).checked=true;
                document.getElementById("C"+a+i+h).style.backgroundColor='yellow';
            }
        }
    }
}
function logic_cl(c) {
    if(document.getElementById("CL"+c).checked) {
        document.getElementById("CLS"+c).style.color='gray';
        document.getElementById("CLS"+c).style.textDecoration='line-through';
    } else {
        document.getElementById("CLS"+c).style.color='black';
        document.getElementById("CLS"+c).style.textDecoration='none';
    }
}
function logic_init() {
    logic_items=new Array();
    for(var i=0;i<logic_res.length;i++) {
        logic_items[logic_res[i]-1000]=1;
    }
    //alert("logic_attrs: "+logic_attrs);
    //alert("logic_size: "+logic_size);
    for(var a=0;a<logic_attrs;a++) {
        for(var i=0;i<logic_size;i++) {
            for(var h=0;h<logic_size;h++) {
                //if(a==1 && i==1 && h==1) alert("C"+a+i+h);
                document.getElementById("C"+a+i+h).style.backgroundColor='white';
                document.getElementById("B"+a+i+h).checked=false;
            }
        }
    }
}

//logic_initialized=false;
function logic_click(n) {
    //if(!logic_initialized) {
        //var a=document.getElementById("B"+n).checked;
        //logic_init();
        //document.getElementById("B"+n).checked=a;
        //logic_initialized=true;
    //}
    var attr=n.substr(0,1);
    var sel=n.substr(1,1);
    var house=n.substr(2,1);
    //alert("click on "+n+" - "+document.getElementById("B"+n).checked);
    var items=new Array();
    var houses=new Array();
    for(var i=0;i<logic_size;i++) {
        items[i]=-1;
        houses[i]=-1;
    }
    for(var i=0;i<logic_size;i++) {
        for(var h=0;h<logic_size;h++) {
            if(document.getElementById("B"+attr+i+h).checked) {
                if(items[i]==-1) items[i]=h;
                else items[i]=-2;
                if(houses[h]==-1) houses[h]=i;
                else houses[h]=-2;
                document.getElementById("C"+attr+i+h).style.backgroundColor='yellow';
            } else {
                document.getElementById("C"+attr+i+h).style.backgroundColor='white';
            }
        }
    }
    for(var i=0;i<logic_size;i++) {
        for(var h=0;h<logic_size;h++) {
            if(houses[h]>=0 && items[houses[h]]>=0 || items[i]>=0 && houses[items[i]]>=0) {
                document.getElementById("C"+attr+i+h).style.backgroundColor='#aaaaff';
            }
        }
    }
}

var logic_spoiled=false;
function logic_check() {
    if(logic_spoiled==false && !confirm("Do you want to proceed, get hints and spoil the fun?")) return;
    logic_spoiled=true;
    for(var a=0;a<logic_attrs;a++) {
        var items=new Array();
        var houses=new Array();
        for(var i=0;i<logic_size;i++) {
            items[i]=-1;
            houses[i]=-1;
        }
        for(var i=0;i<logic_size;i++) {
            for(var h=0;h<logic_size;h++) {
                if(document.getElementById("B"+a+i+h).checked) {
                    if(logic_items[a*100+i*10+h]==0) {
                        items[i]=-2;
                        houses[h]=-2;
                    }
                    if(items[i]==-1) items[i]=h;
                    else items[i]=-2;
                    if(houses[h]==-1) houses[h]=i;
                    else houses[h]=-2;
                } else {
                    if(logic_items[a*100+i*10+h]==1) {
                        items[i]=-2;
                        houses[h]=-2;
                    }
                }
                document.getElementById("C"+a+i+h).style.backgroundColor='red';
            }
        }
        for(var i=0;i<logic_size;i++) {
            for(var h=0;h<logic_size;h++) {
                if(houses[h]>=0 && items[houses[h]]>=0 || items[i]>=0 && houses[items[i]]>=0) {
                    document.getElementById("C"+a+i+h).style.backgroundColor='#aaffaa';
                }
            }
        }
    }
}

function logic_ok() {
    var error=false;
    for(var a=0;a<logic_attrs && !error;a++) {
        for(var i=0;i<logic_size && !error;i++) {
            for(var h=0;h<logic_size && !error;h++) {
                if(document.getElementById("B"+a+i+h).checked) {
                    if(logic_items[a*100+i*10+h]==0) {
                        error=true;
                    }
                } else {
                    if(logic_items[a*100+i*10+h]==1) {
                        error=true;
                    }
                }
            }
        }
    }
    if(error) {
        alert("Unforunately the solution is incomplete and/or wrong.");
        return;
    }
    for(var a=0;a<logic_attrs;a++) {
        for(var i=0;i<logic_size;i++) {
            for(var h=0;h<logic_size;h++) {
                if(logic_items[a*100+i*10+h]==1) {
                    document.getElementById("C"+a+i+h).style.backgroundColor='green';
                } else {
                    document.getElementById("C"+a+i+h).style.backgroundColor='white';
                }
            }
        }
    }
    alert("Congratulations!");
}

