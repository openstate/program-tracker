head.ready(function()
{
    rangy.init()

    /* 
     * functions
     */

    var Topic = {
        hideHighlight: function()
        {
            $('#program').append($('#topiclabel'));
            $('.highlight').each(function(){
                $(this).replaceWith($(this).html());
            });
            $('#topiclabel').hide();
        },
        
        highlight: function(container)
        {
            var start = $(this).attr('topic:start');
            var end = $(this).attr('topic:end');

            //console.log('start:' + start + '   -- end : ' + end);

            //create range
            range = rangy.createRange();

            if (end < 0) 
            {
                range.selectNode(container)
            }
            else
            {
                range.selectCharacters(container, start, end)
            }

            //apply highlight
            Topic.highlightApplier.applyToRange(range);
        },

        hoverHighlight: function()
        {
            var container = $(this).parents('div.p').children('p').get(0);
            Topic.highlight.call(this,container)
        },

        highlightApplier: rangy.createCssClassApplier("highlight")

    }

    /*
     * selectors
     */

    //hide selection
    $('div.p').mousedown(Topic.hideHighlight);

    // do selection
    $('div.p').mouseup(function()
    {
        Topic.hideHighlight();

        myRange = rangy.getSelection();

        //return if nothing selected
        if (myRange.isCollapsed)
            return;

        //expand to whole words
        myRange.expand('word')

        //highlight
        Topic.highlightApplier.applyToSelection()

        var selection = myRange.saveCharacterRanges(this); 
        var startOffset = selection[0].range.start-1; //offset by one for some reason
        var endOffset = selection[0].range.end-1; //idem

        //console.log('start:' + startOffset + '   -- end : ' + endOffset);

        $('input[name=start]').val(startOffset);
        $('input[name=end]').val(endOffset);
        $('input[name=pid]').val(this.id);
        $('.highlight').last().append($('#topiclabel'));
        $('#topiclabel').show();
        $('input[name=label]').focus();
    });
  
    //submit on enter
    $('#topiclabel input').keypress(function(e){
        if(e.which == 13) {
            $( "input[name=label]" ).autocomplete('close'); //close autocomplete
            $('#topiclabel form').submit();
            return false;
        }
    });
    
    //check and submit formdata
    $('#topiclabel form').ajaxForm({
        beforeSubmit: function(formData) {
            for (var i=0; i < formData.length; i++) { 
                if (!formData[i].value) { 
                    return false; 
                } 
            }                
        },
        dataType: 'json',
        clearForm: true,
        success: function(data) {
            if(data.id)
            {
                var element = $('#topiclabel').parents('div.p').children('.topics');
                var newLabel = $('<div style="background-color: '+data.source_color+'" class="topic" id="'+data.id+'"  topic:start="'+data.start+'" topic:end="'+data.end+'" title="'+data.topic_desc+'"><a href="/topic/'+data.topic_id+'/">'+data.label+'</a></div>');

                newLabel.hover(Topic.hoverHighlight, Topic.hideHighlight).appendTo(element);
            }
            
            Topic.hideHighlight();
        },
    });

    $('.selected').each(function()
    {
        Topic.highlight.call(this,this)
    })
    
    //hovers for topics
    $('.topic').hover(Topic.hoverHighlight, Topic.hideHighlight);
    
    $( "input[name=label]" ).autocomplete({
            source: "/topic/getTopics/"
    });
});