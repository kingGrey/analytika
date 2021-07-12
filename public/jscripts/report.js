//Further documentation found and retrieved from below link
//documentation: http://www.lib4dev.in/info/jonmiles/bootstrap-treeview/15324383

var defaultData = {}    // hold tree structure

// on page load preload all report items
// found in destination folder
window.onload = function(){
//    alert('loading...')
    fetch('/report_details')
    .then(response => response.json())
    .then(data=>{
        defaultData = data.value
        console.log(data);
        $('#treeview1').treeview({
            levels:1,
            data: defaultData,
            enableLinks: false,
            collapseIcon:'fas fa-minus-square',
            expandIcon:'fas fa-plus-circle',
            showIcon: true,
            showTags: false,
            backColor: "#242526",
            color:"#FFFFFF",
            onhoverColor: "#445387",
            selectedColor: "#F5F5F5",
            onNodeSelected: function(event, data){
                if (data.text.includes(".html")){
//                    alert('Name:'+data.href)
                    document.getElementById("linker_content").innerHTML=`<object type="text/html" data=${data.href} width="100%" height="100%" style="overflow: scroll;"></object>`;
                }
            }
        });
    })
    .catch(function(error) {
      console.log(error);
    });
}

function getTree() {
  // Some logic to retrieve, or generate tree structure
  return defaultData;
}

// searchable trees setup
var $searchableTree = $('#treeview1').treeview({
   data: getTree(),
         enableLinks: false,
         collapseIcon:'fas fa-minus-square',
         expandIcon:'fas fa-plus-circle',
         showIcon: true,
         showTags: false,
         backColor: "#242526",
         color:"#FFFFFF",
         onhoverColor: "#445387",
         selectedColor: "#F5F5F5",
});

$(function () {
    var selectors = {
        'tree': '#treeview1',
        'input': '#input-search',
        'reset': '#btn-clear-search'
    };
    var lastPattern = ''; // closure variable to prevent redundant operation

    // collapse and enable all before search
    function reset(tree) {
        tree.collapseAll();
        tree.enableAll();
    }

    // disable all nodes not related to search criteria
    function collectUnrelated(nodes) {
        var unrelated = [];
        $.each(nodes, function (i, n) {
            if (!n.searchResult && !n.state.expanded) { // no hit, no parent
                unrelated.push(n.nodeId);
            }
            if (!n.searchResult && n.nodes) { // recurse for non-result children
                $.merge(unrelated, collectUnrelated(n.nodes));
            }
        });
        return unrelated;
    }

    // search callback
    var search = function (e) {
        var pattern = $(selectors.input).val();
        if (pattern === lastPattern) {
            return;
        }
        lastPattern = pattern;
        var tree = $(selectors.tree).treeview(true);
        reset(tree);
        if (pattern.length < 3) { // avoid heavy operation
            tree.clearSearch();
        } else {
            tree.search(pattern);
            // get all root nodes: node 0 who is assumed to be
            // a root node, and all siblings of node 0.
            var roots = tree.getSiblings(0);
            roots.push(tree.getNode(0));
            //collect all nodes to disable  and disable all.
            var unrelated = collectUnrelated(roots);
            tree.disableNode(unrelated, {silent: true});
        }
    };

    // track typing in search input - monitor keyup
    $(selectors.input).on('keyup', search);

    // clear button clicked - reset items
    $(selectors.reset).on('click', function (e) {
        $(selectors.input).val('');
        var tree = $(selectors.tree).treeview(true);
        reset(tree);
        tree.clearSearch();
    });
});
