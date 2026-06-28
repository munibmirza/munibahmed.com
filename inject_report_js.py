with open('InterAudit-P1.html', encoding='utf-8') as f:
    content = f.read()

JS_BLOCK_START = 175227  # the // ====== comment
JS_BLOCK_END   = 195216  # after })();

NEW_JS = """// ================================================================
// REPORT -- CS Audit Working Paper (Database-driven)
// ================================================================
  (function () {
    'use strict';

    const DIVS = ['AC','REF','WD','WM','OVEN','LED','OTHER'];

    let shlDb = [];

    function newRow(div,type,status,warranty,age,revenue,unit,part) {
      return {
        div: div||'AC', type: type||'IH', status: status||'Resolved',
        warranty: warranty||'With', age: parseFloat(age)||0,
        revenue: parseFloat(revenue)||0, unit: !!unit, part: !!part
      };
    }

    function renderDb() {
      var tbody = $('#shlDbBody'); tbody.empty();
      shlDb.forEach(function(row, i) {
        var divOpts = DIVS.map(function(d){ return '<option '+(row.div===d?'selected':'')+'>'+d+'</option>'; }).join('');
        tbody.append('<tr data-ri="'+i+'">' +
          '<td class="text-center px-2 py-1 text-blue-100/40">'+(i+1)+'</td>' +
          '<td class="px-1 py-0.5"><select class="shl-db-sel" data-ri="'+i+'" data-f="div" style="width:68px">'+divOpts+'</select></td>' +
          '<td class="px-1 py-0.5"><select class="shl-db-sel" data-ri="'+i+'" data-f="type" style="width:105px">' +
            '<option '+(row.type==='IH'?'selected':'')+' value="IH">In-House</option>' +
            '<option '+(row.type==='CWS'?'selected':'')+' value="CWS">Contract WS</option>' +
          '</select></td>' +
          '<td class="px-1 py-0.5"><select class="shl-db-sel" data-ri="'+i+'" data-f="status" style="width:92px">' +
            '<option '+(row.status==='Resolved'?'selected':'')+'>Resolved</option>' +
            '<option '+(row.status==='Cancelled'?'selected':'')+'>Cancelled</option>' +
            '<option '+(row.status==='Pending'?'selected':'')+'>Pending</option>' +
          '</select></td>' +
          '<td class="px-1 py-0.5"><select class="shl-db-sel" data-ri="'+i+'" data-f="warranty" style="width:122px">' +
            '<option '+(row.warranty==='With'?'selected':'')+' value="With">With Warranty</option>' +
            '<option '+(row.warranty==='Partial'?'selected':'')+' value="Partial">Partial Warranty</option>' +
            '<option '+(row.warranty==='Without'?'selected':'')+' value="Without">Without Warranty</option>' +
          '</select></td>' +
          '<td class="px-1 py-0.5"><input type="number" class="shl-input-sm shl-db-num" data-ri="'+i+'" data-f="age" value="'+row.age+'" min="0" style="width:60px;text-align:center"/></td>' +
          '<td class="px-1 py-0.5"><input type="number" class="shl-input-sm shl-db-num" data-ri="'+i+'" data-f="revenue" value="'+row.revenue+'" min="0" style="width:82px;text-align:right"/></td>' +
          '<td class="text-center px-1 py-0.5"><input type="checkbox" class="shl-db-chk" data-ri="'+i+'" data-f="unit" '+(row.unit?'checked':'')+'/></td>' +
          '<td class="text-center px-1 py-0.5"><input type="checkbox" class="shl-db-chk" data-ri="'+i+'" data-f="part" '+(row.part?'checked':'')+'/></td>' +
          '<td class="text-center px-1 py-0.5"><button class="shl-del-row text-red-400 hover:text-red-300 text-sm px-2" data-ri="'+i+'">x</button></td>' +
        '</tr>');
      });
      $('#shlRowCount').text(shlDb.length + ' records');
    }

    window.shlCompute = function() {
      var notif={total:{},cancelled:{},resolved:{},pending:{}};
      var warr={With:{},Partial:{},Without:{}};
      var aging={IH:[0,0,0,0],CWS:[0,0,0,0]};
      var repU={},repP={};
      DIVS.forEach(function(d){
        notif.total[d]=0; notif.cancelled[d]=0; notif.resolved[d]=0; notif.pending[d]=0;
        warr.With[d]=0; warr.Partial[d]=0; warr.Without[d]=0;
        repU[d]=0; repP[d]=0;
      });
      var svcRev=0, partsRev=0;

      shlDb.forEach(function(r){
        var d=DIVS.includes(r.div)?r.div:'OTHER';
        notif.total[d]++;
        if(r.status==='Cancelled') notif.cancelled[d]++;
        else if(r.status==='Resolved') notif.resolved[d]++;
        else notif.pending[d]++;
        (warr[r.warranty]||warr.With)[d]++;
        var ab=r.age<=3?0:r.age<=7?1:r.age<=10?2:3;
        aging[r.type==='CWS'?'CWS':'IH'][ab]++;
        if(r.unit) repU[d]++;
        if(r.part) repP[d]++;
        if(r.part) partsRev+=parseFloat(r.revenue)||0;
        else svcRev+=parseFloat(r.revenue)||0;
      });
      DIVS.forEach(function(d){ notif.pending[d]=notif.total[d]-notif.cancelled[d]-notif.resolved[d]; });

      // Notification Analysis
      var notifDefs=[['Total Notifications',notif.total,''],['Cancelled',notif.cancelled,''],['Resolved',notif.resolved,''],['Pending',notif.pending,'font-semibold text-yellow-300']];
      var nb=$('#shlRNotifBody').empty();
      notifDefs.forEach(function(nd){
        var cells=DIVS.map(function(d){return '<td class="text-center px-3 py-1.5 '+nd[2]+'">'+(nd[1][d]||0).toLocaleString()+'</td>';}).join('');
        var tot=DIVS.reduce(function(s,d){return s+(nd[1][d]||0);},0);
        nb.append('<tr><td class="px-4 py-1.5 text-sm '+nd[2]+'">'+nd[0]+'</td>'+cells+'<td class="text-center px-3 py-1.5 font-bold">'+tot.toLocaleString()+'</td></tr>');
      });
      var totAll=DIVS.reduce(function(s,d){return s+(notif.total[d]||0);},0);
      var days=parseFloat($('#shl_days').val())||1;
      var ihC=shlDb.filter(function(r){return r.type!=='CWS';}).length;
      var cwsC=shlDb.filter(function(r){return r.type==='CWS';}).length;
      var pendAll=DIVS.reduce(function(s,d){return s+(notif.pending[d]||0);},0);
      $('#shlNotifStats').html(
        '<div class="glass p-3 rounded-xl text-center"><p class="text-xs text-blue-100/60">Cases / Day</p><p class="text-2xl font-bold text-yellow-300">'+( totAll/days).toFixed(1)+'</p></div>' +
        '<div class="glass p-3 rounded-xl text-center"><p class="text-xs text-blue-100/60">In-House vs Contract</p><p class="text-lg font-bold text-blue-200">'+ihC.toLocaleString()+' <span class="text-blue-100/40">vs</span> '+cwsC.toLocaleString()+'</p></div>' +
        '<div class="glass p-3 rounded-xl text-center"><p class="text-xs text-blue-100/60">Pending</p><p class="text-2xl font-bold text-red-400">'+pendAll+'</p></div>'
      );

      // Warranty
      var wDefs=[['With Warranty','With'],['Partial Warranty','Partial'],['Without Warranty','Without'],['Total',null]];
      var wb2=$('#shlRWarrantyBody').empty();
      wDefs.forEach(function(wd){
        var tot=0;
        var cells=DIVS.map(function(d){
          var v=wd[1]?(warr[wd[1]][d]||0):(warr.With[d]||0)+(warr.Partial[d]||0)+(warr.Without[d]||0);
          tot+=v; return '<td class="text-center px-3 py-1.5 '+(wd[1]?'':'font-bold')+'">'+v.toLocaleString()+'</td>';
        }).join('');
        wb2.append('<tr><td class="px-4 py-1.5 text-sm '+(wd[1]?'':'font-bold')+'">'+wd[0]+'</td>'+cells+'<td class="text-center px-3 py-1.5 font-bold">'+tot.toLocaleString()+'</td></tr>');
      });

      // Aging
      var agLbls=['0 - 3 Days','4 - 7 Days','8 - 10 Days','Above 10 Days'];
      var ab2=$('#shlRAgingBody').empty();
      var tIH=aging.IH.reduce(function(s,v){return s+v;},0)||1;
      var tCWS=aging.CWS.reduce(function(s,v){return s+v;},0)||1;
      agLbls.forEach(function(lbl,i){
        var ih=aging.IH[i],cw=aging.CWS[i];
        ab2.append('<tr><td class="px-4 py-1.5 text-sm">'+lbl+'</td>' +
          '<td class="text-center px-3 py-1.5">'+ih.toLocaleString()+'</td>' +
          '<td class="text-center px-3 py-1.5">'+(ih/tIH*100).toFixed(1)+'%</td>' +
          '<td class="text-center px-3 py-1.5">'+cw.toLocaleString()+'</td>' +
          '<td class="text-center px-3 py-1.5">'+(cw/tCWS*100).toFixed(1)+'%</td>' +
          '<td class="text-center px-3 py-1.5 font-semibold">'+(ih+cw).toLocaleString()+'</td></tr>');
      });
      var sIH=aging.IH.reduce(function(s,v){return s+v;},0);
      var sCWS=aging.CWS.reduce(function(s,v){return s+v;},0);
      ab2.append('<tr class="font-bold"><td class="px-4 py-2">Total</td>' +
        '<td class="text-center px-3 py-2">'+sIH.toLocaleString()+'</td><td class="text-center px-3 py-2">100%</td>' +
        '<td class="text-center px-3 py-2">'+sCWS.toLocaleString()+'</td><td class="text-center px-3 py-2">100%</td>' +
        '<td class="text-center px-3 py-2">'+(sIH+sCWS).toLocaleString()+'</td></tr>');

      // Units/Parts
      var rb=$('#shlRReplacedBody').empty();
      [['Units Replaced',repU],['Parts Replaced',repP]].forEach(function(rd){
        var cells=DIVS.map(function(d){return '<td class="text-center px-3 py-1.5">'+(rd[1][d]||0)+'</td>';}).join('');
        var tot=DIVS.reduce(function(s,d){return s+(rd[1][d]||0);},0);
        rb.append('<tr><td class="px-4 py-1.5 text-sm">'+rd[0]+'</td>'+cells+'<td class="text-center px-3 py-1.5 font-bold">'+tot+'</td></tr>');
      });

      // Revenue
      var prevRev=parseFloat($('#shl_prev_rev').val())||0;
      var prevParts=parseFloat($('#shl_prev_parts').val())||0;
      var revDefs=[
        {label:'Service Revenue',cur:svcRev,prev:prevRev},
        {label:'Parts Revenue',cur:partsRev,prev:prevParts},
        {label:'Total Revenue',cur:svcRev+partsRev,prev:prevRev+prevParts}
      ];
      var rvb=$('#shlRRevenueBody').empty();
      revDefs.forEach(function(r){
        var v=r.cur-r.prev, vp=r.prev?(v/r.prev*100).toFixed(1)+'%':'-';
        var col=v<0?'#f87171':'#86efac';
        rvb.append('<tr><td class="px-4 py-1.5 text-sm">'+r.label+'</td>' +
          '<td class="text-center px-3 py-1.5">'+r.cur.toLocaleString('en-PK')+'</td>' +
          '<td class="text-center px-3 py-1.5">'+r.prev.toLocaleString('en-PK')+'</td>' +
          '<td class="text-center px-3 py-1.5" style="color:'+col+'">'+(v>=0?'+':'')+v.toLocaleString('en-PK')+'</td>' +
          '<td class="text-center px-3 py-1.5" style="color:'+col+'">'+vp+'</td></tr>');
      });
    };

    // Row management
    $('#shlAddRow').on('click', function(){ shlDb.push(newRow()); renderDb(); window.shlCompute(); });
    $('#shlClearDb').on('click', function(){
      if(!confirm('Clear all '+shlDb.length+' records?')) return;
      shlDb=[]; renderDb(); window.shlCompute();
    });
    $(document).on('click','.shl-del-row',function(e){
      e.stopPropagation();
      shlDb.splice(parseInt($(this).data('ri')),1); renderDb(); window.shlCompute();
    });
    $(document).on('change','#shlDbTable .shl-db-sel',function(){
      var i=parseInt($(this).data('ri')); shlDb[i][$(this).data('f')]=$(this).val(); window.shlCompute();
    });
    $(document).on('input','#shlDbTable .shl-db-num',function(){
      var i=parseInt($(this).data('ri')); shlDb[i][$(this).data('f')]=parseFloat($(this).val())||0; window.shlCompute();
    });
    $(document).on('change','#shlDbTable .shl-db-chk',function(){
      var i=parseInt($(this).data('ri')); shlDb[i][$(this).data('f')]=$(this).prop('checked'); window.shlCompute();
    });
    $(document).on('input change','#shl_prev_rev,#shl_prev_parts',window.shlCompute);

    // Tabs
    $(document).on('click','[data-shl-tab]',function(){
      $('[data-shl-tab]').removeClass('active'); $(this).addClass('active');
      $('.shl-pane').addClass('hidden'); $('#'+$(this).data('shl-tab')).removeClass('hidden');
    });

    // Excel Import
    function parseDiv(s){
      s=String(s||'').trim().toUpperCase();
      if(/^AC$|AIR.*CON/i.test(s)) return 'AC';
      if(/^REF$|REFRIG/i.test(s)) return 'REF';
      if(/^WD$|WASH.*DRY|DRYER/i.test(s)) return 'WD';
      if(/^WM$|WASH.*MAC/i.test(s)) return 'WM';
      if(/^OVEN$|MICRO/i.test(s)) return 'OVEN';
      if(/^LED$|\\bTV\\b|TELE/i.test(s)) return 'LED';
      if(DIVS.includes(s)) return s;
      return 'OTHER';
    }

    $('#shlDbImport').on('change',function(e){
      var file=e.target.files[0]; if(!file) return;
      var reader=new FileReader();
      reader.onload=function(ev){
        try{
          var wb=XLSX.read(ev.target.result,{type:'array'});
          var wsName=['DataBase','Database','database'].find(function(n){return wb.SheetNames.includes(n);})||wb.SheetNames[0];
          var raw=XLSX.utils.sheet_to_json(wb.Sheets[wsName],{header:1,defval:''});
          var hRow=-1;
          for(var r=0;r<Math.min(15,raw.length);r++){
            var rowUp=raw[r].map(function(c){return String(c).trim().toUpperCase();});
            if(rowUp.some(function(h){return /DIV|PRODUCT|CATEG/.test(h);})||rowUp.some(function(h){return /^AC$|^REF$/.test(h);})){
              hRow=r; break;
            }
          }
          var newRows=[];
          if(hRow>=0){
            var hdrs=raw[hRow].map(function(c){return String(c).trim().toUpperCase();});
            function col(pat){return hdrs.findIndex(function(h){return pat.test(h);});}
            var cDiv=col(/DIV|PRODUCT|CATEG/), cType=col(/SERVICE.*TYPE|^TYPE$|^IH$|^CWS$/);
            var cStat=col(/STATUS|STAT/), cWarr=col(/WARRANTY|WARR/), cAge=col(/^AGE$|AGE.*DAY|NO.*DAY/);
            var cRev=col(/REV|AMT|AMOUNT/), cUnit=col(/UNIT.*REP/), cPart=col(/PART.*REP/);
            for(var ri=hRow+1;ri<raw.length;ri++){
              var row=raw[ri];
              if(!row[cDiv>=0?cDiv:0]) continue;
              var div=parseDiv(cDiv>=0?row[cDiv]:row[0]);
              var typeRaw=String(cType>=0?row[cType]:'').toUpperCase();
              var type=/CWS|CONTRACT|CW/.test(typeRaw)?'CWS':'IH';
              var statRaw=String(cStat>=0?row[cStat]:'').toLowerCase();
              var status=/cancel/.test(statRaw)?'Cancelled':/pend|open/.test(statRaw)?'Pending':'Resolved';
              var wRaw=String(cWarr>=0?row[cWarr]:'').toLowerCase();
              var warr2=/partial/.test(wRaw)?'Partial':/without|no.?warr/.test(wRaw)?'Without':'With';
              var age=cAge>=0?(parseFloat(row[cAge])||0):0;
              var revenue=cRev>=0?(parseFloat(row[cRev])||0):0;
              var unit=cUnit>=0?/y|yes|1|true/i.test(String(row[cUnit])):false;
              var part=cPart>=0?/y|yes|1|true/i.test(String(row[cPart])):false;
              newRows.push(newRow(div,type,status,warr2,age,revenue,unit,part));
            }
          } else {
            for(var ri2=1;ri2<raw.length;ri2++){
              var r2=raw[ri2].filter(function(c){return c!==''&&c!==null;});
              if(r2.length<3) continue;
              newRows.push(newRow(parseDiv(r2[0]),/CWS|CONTRACT/i.test(String(r2[1]))?'CWS':'IH',
                /cancel/i.test(String(r2[2]))?'Cancelled':/pend|open/i.test(String(r2[2]))?'Pending':'Resolved',
                /partial/i.test(String(r2[3]))?'Partial':/without/i.test(String(r2[3]))?'Without':'With',
                parseFloat(r2[4])||0,parseFloat(r2[5])||0));
            }
          }
          shlDb=newRows; renderDb(); window.shlCompute();
          alert('Imported '+newRows.length+' records from "'+wsName+'".');
        }catch(err){alert('Import error: '+err.message);}
      };
      reader.readAsArrayBuffer(file);
    });

    // Excel Export
    $('#shlExportExcel').on('click',function(){
      if(!shlDb.length){alert('No records to export.');return;}
      var wb2=XLSX.utils.book_new();
      var aoa=[['Sr.','Division','Service Type','Status','Warranty','Age (Days)','Revenue (Rs.)','Unit Replaced','Part Replaced']];
      shlDb.forEach(function(r,i){aoa.push([i+1,r.div,r.type==='CWS'?'Contract WS':'In-House',r.status,r.warranty+' Warranty',r.age,r.revenue,r.unit?'Yes':'No',r.part?'Yes':'No']);});
      XLSX.utils.book_append_sheet(wb2,XLSX.utils.aoa_to_sheet(aoa),'DataBase');
      [['shlRNotifBody','Notification Analysis'],['shlRWarrantyBody','Warranty Analysis'],
       ['shlRAgingBody','Aging Schedule'],['shlRReplacedBody','Units Parts'],['shlRRevenueBody','Revenue']
      ].forEach(function(nd){
        var aoa2=[]; $('#'+nd[0]).closest('table').find('tr').each(function(){
          var row=[]; $(this).find('th,td').each(function(){row.push($(this).text().trim());}); aoa2.push(row);
        });
        XLSX.utils.book_append_sheet(wb2,XLSX.utils.aoa_to_sheet(aoa2),nd[1]);
      });
      XLSX.writeFile(wb2,'Report_'+($('#shl_branch').val()||'SC').replace(/\\s+/g,'_')+'.xlsx');
    });

    // Feed to Audit Report
    $('#shlFeedReport').on('click',function(){
      if(typeof arNotifData==='undefined'){
        window.location.hash='#/audit-report';
        setTimeout(function(){alert('Navigate back to Report and click Feed again after Audit Report loads.');},600);
        return;
      }
      var P5=['AC','REF','WD','WM','OVEN','LED'];
      var nT={},nC={},nR={},wW={},wPa={},wWo={},rU={},rP={};
      P5.forEach(function(d){nT[d]=0;nC[d]=0;nR[d]=0;wW[d]=0;wPa[d]=0;wWo[d]=0;rU[d]=0;rP[d]=0;});
      shlDb.forEach(function(r){
        var d=P5.includes(r.div)?r.div:null; if(!d) return;
        nT[d]++;
        if(r.status==='Cancelled')nC[d]++;
        else if(r.status==='Resolved')nR[d]++;
        if(r.warranty==='With')wW[d]++;
        else if(r.warranty==='Partial')wPa[d]++;
        else wWo[d]++;
        if(r.unit)rU[d]++;
        if(r.part)rP[d]++;
      });
      arNotifData.total     =P5.map(function(d){return nT[d];});
      arNotifData.cancelled =P5.map(function(d){return nC[d];});
      arNotifData.resolved  =P5.map(function(d){return nR[d];});
      arWarrantyData.withW   =P5.map(function(d){return wW[d];});
      arWarrantyData.partialW=P5.map(function(d){return wPa[d];});
      arWarrantyData.withoutW=P5.map(function(d){return wWo[d];});
      arReplacedData.units=P5.map(function(d){return rU[d];});
      arReplacedData.parts=P5.map(function(d){return rP[d];});
      var sR=0,pR=0;
      shlDb.forEach(function(r){if(r.part)pR+=r.revenue||0;else sR+=r.revenue||0;});
      if(typeof arRevenueData!=='undefined'){
        arRevenueData[0]={label:'Service Revenue',cur:sR,  prev:(arRevenueData[0]?arRevenueData[0].prev:0)};
        arRevenueData[1]={label:'Parts Revenue',  cur:pR,  prev:(arRevenueData[1]?arRevenueData[1].prev:0)};
        arRevenueData[2]={label:'Total Revenue',  cur:sR+pR,prev:(arRevenueData[2]?arRevenueData[2].prev:0)};
      }
      $('#ar_branch').val($('#shl_branch').val()||'');
      $('#ar_cur_from').val($('#shl_from').val()||'');
      $('#ar_cur_to').val($('#shl_to').val()||'');
      $('#ar_prev_from').val($('#shl_pfrom').val()||'');
      $('#ar_prev_to').val($('#shl_pto').val()||'');
      $('#ar_days').val($('#shl_days').val()||'');
      window.location.hash='#/audit-report';
      setTimeout(function(){
        if(typeof rebuildAllAnalysis==='function') rebuildAllAnalysis();
        alert('Done! Data fed to Audit Report. Check the Analysis tab, then click Generate Report.');
      },400);
    });

    // Init
    function initShlDb(){ renderDb(); window.shlCompute(); }
    var shlDbInited=false;
    $(window).on('hashchange',function(){
      if(location.hash==='#/shl-report-db'&&!shlDbInited){shlDbInited=true;setTimeout(initShlDb,50);}
    });
    if(location.hash==='#/shl-report-db'&&!shlDbInited){shlDbInited=true;setTimeout(initShlDb,50);}

  })();"""

content = content[:JS_BLOCK_START] + NEW_JS + content[JS_BLOCK_END:]
with open('InterAudit-P1.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done. Size:', len(content))
