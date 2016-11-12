/*
 Highchart frames for my personal budget app

 Author: Christian Schneider <cmf.schneider@posteo.de>
 version = 1.0.0.

*/

// Daily Chart
function time_chart(chartId, chartDataUrl, title, tableFrameId, tableId,
                    tableDataUrl, piChartL, piChartR) {
  var chartPars = {
    chart : {
      zoomType : 'x',
      renderTo : chartId,
      events: {
        selection: function(event) {
          if(event.xAxis != null) {
            // Update charts and table for selected range
            startDate = Math.round(event.xAxis[0].min/1000);
            endDate = Math.round(event.xAxis[0].max/1000);
            updateCharts(startDate, endDate, chartId, chartDataUrl, 
                         tableFrameId, tableId, tableDataUrl, piChartL, 
                         piChartR);
          }
          if(event.resetSelection) {
            // Reset tables and charts
            updateCharts(null, null, chartId, chartDataUrl, tableFrameId, 
                         tableId, tableDataUrl, piChartL, piChartR);
          }
    }}},          
    title : { text : title },
    plotOptions : {
      area : {
        fillColor: {
          linearGradient: {
            x1: 0,
            y1: 0,
            x2: 0,
            y2: 1
          },
          stops: [
            [0, Highcharts.getOptions().colors[0]],
            [1, Highcharts.Color(Highcharts.getOptions().colors[0])
                          .setOpacity(0).get('rgba')]
          ]
        },
        marker: { radius: 2 },
        lineWidth: 1,
        states: {
          hover: { lineWidth: 1 }
        },
        threshold: null
    }},
    xAxis : { type : 'datetime'},
    legend : { enabled : false },
    series: [{
      type: 'area',
  }]}
  chartPars.series[0].data = $.getMyJSON(chartDataUrl)
  return new Highcharts.Chart(chartPars);
}  

function buildTable(frameId, view_href, editUrl) {
  // Options for editing the table
  var editOptions = {
    keys: true,
    aftersavefunc: function() {
        $(frameId).jqGrid('setGridParam',{datatype:'json'})
                  .trigger("reloadGrid");
  }};
  
  $(frameId).jqGrid({
    url: view_href,
    mtype: "GET",
    datatype: "json",
    colModel: [
      { label : 'Name', name : 'Name', width : 100, editable : true },
      { label : 'Amount', name : 'Amount', width : 40, formatter : 'currency', 
        align : 'right', sorttype : 'currency', editable : true },
      { label : 'CUR', name : 'CUR', width : 20, align : 'center', 
        editable :true },
      { label : 'Date', name : 'Date', width : 50, align : 'center', 
        editable:true },
      { label : 'Category', name : 'Category', width : 70, editable :true},
      { label : 'Comment', name : 'Comment', width : 70, editable : true},
      { label : 'Reference', name : 'Reference', width : 150, editable :true },
      { index : 'id', label : 'id', name : 'id', width : 0.1, hidden : true}
    ],
    rowList: [],        // disable page size dropdown
    pgbuttons: false,     // disable page control like next, back button
    pgtext: null,         // disable pager text like 'Page 0 of 10'
    viewrecords: false,    // disable current view record text View 1-10 of 100' 
    viewrecords: true,
    autowidth: true,
    shrinktofit: true,
    height: '100%',
    rowNum: 100,
    loadonce: true,
    pager: pager,
    sortname: 'Date',
    sortorder: "desc",
    onSelectRow: function(id) { 
      buildTable(frameId, view_href, editUrl)
      if(id && id!==lastsel){ 
        jQuery(frameId).jqGrid('restoreRow',lastsel); 
        jQuery(frameId).jqGrid('editRow',id,true); 
        lastsel=id; } }, 
    editurl: editUrl,
    //editData: { csrfmiddlewaretoken: '{{ csrf_token }}'},
  });
  $(frameId).parents('div.ui-jqgrid-bdiv').css("max-height","300px");
  // Hide pk field
  $(frameId).jqGrid('navGrid',pager,{edit:false,add:false,del:true});
  $(frameId).jqGrid('inlineNav',pager, {
    addParams : {
        addRowParams: editOptions
    },
    editParams: editOptions        
  });
}

function pi_chart(chartId, chartDataUrl, title, tableFrameId, tableId, 
                  tableDataUrl) {
  // Set the parameters
  var chartPars = {
    chart : { renderTo : chartId },
    title : { text : title },
    plotOptions : {
      pie : {
        allowPointSelect : true,
        point : {
          events : {
            click : function(event) {
              // Check if table is already present and create DIV and datatable
              //$.jgrid.gridUnload(tableId);
              $(tableId).jqGrid("GridUnload");
              $(tableId + 'Pager').remove();
              $(tableId).remove();

              // Plot selected category transaction in table
              if( openTable !== 'CAT' + this.name) {
                openTable = 'CAT' + this.name;
                tableHTML = "<div class='jQueryUI'><table id=" + 
                            tableId.substring(1) + 
                            "></table><div id=" +
                            tableId.substring(1)+"Pager></div></div>";
                $(tableFrameId).append(tableHTML);
                tableData = tableDataUrl + this.name + "/";
                buildTable(tableId, tableData, editUrl);
              }
              // Deletes table if already present (double click on that entry)
              else { 
                openTable = '';
                tableHTML = "<div class='jQueryUI'><table id=" + 
                            tableId.substring(1) + 
                            "></table><div id=" + 
                            tableId.substring(1)+"Pager></div></div>"
                $(tableFrameId).append(tableHTML);
               }
        }}},
        cursor : 'pointer',
        dataLabels : {
          enabled : true,
          format : '<b>{point.name}</b>: {point.percentage:.1f} %',
          style: {
            color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 
                   'black'
    }}}},
    tooltip: {
      pointFormat: '<span style="color: {point.color}">\u25CF</span> ' +
                   title + ': <b>{point.y: .2f}</b>€ </span>',
    },
    series: [{
        type: 'pie',
    }]
  }
  chartPars.series[0].data = $.getMyJSON(chartDataUrl)
  
  return new Highcharts.Chart(chartPars);
}

function updateCharts(startDate, endDate, chartId, chartDataUrl, tableFrameId, 
                      tableId, tableDataUrl, piChartL, piChartR) {
  // Reset table
  $(tableId).jqGrid("GridUnload");
  $(tableId + 'Pager').remove();
  $(tableId).remove();
  // Plot selected date transaction in table
  var piChartUrlR = indexUrl + "ChartData/Ausgaben/";
  var piChartUrlL = indexUrl + "ChartData/Einnahmen/";
  var dateRange = "";
  // Check for data range
  if (startDate != null && endDate != null ){
    dateRange = String(startDate) + "-" + String(endDate);
    piChartUrlR = piChartUrlR + dateRange;
    piChartUrlL = piChartUrlL + dateRange; 
    tableDataUrl = tableDataUrl + "range/";
  }
  // Create Table
  if( openTable !== 'Date' + dateRange && dateRange != '')  {
    openTable = 'Date' + dateRange; 
    tableHTML = "<div class='jQueryUI'><table id=" + 
                tableId.substring(1) + 
                "></table><div id=" +
                tableId.substring(1)+"Pager></div></div>";
    $(tableFrameId).append(tableHTML);
    tableData = tableDataUrl + dateRange; 
    buildTable(tableId, tableData, editUrl);
    }
  // Deletes table if already present (double click on that entry)
  else { 
    openTable = '';
    tableHTML = "<div class='jQueryUI'><table id=" + 
                tableId.substring(1) + 
                "></table><div id=" + 
                tableId.substring(1)+"Pager></div></div>"
    $(tableFrameId).append(tableHTML);
  }
  // Update Pi Chart for Time Range
  piChartR.series[0].setData($.getMyJSON(piChartUrlR), true);
  piChartL.series[0].setData($.getMyJSON(piChartUrlL), true);
}

$.extend({
  getMyJSON : function(url) {
    var theResponse = null;
    $.ajax({
      url : url,
      dataType : "json",
      async : false,
      success : function(resp) {
        theResponse = resp;
      }
    });
    return theResponse;
  }
});