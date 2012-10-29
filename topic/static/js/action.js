var Topic = {
	hideHighlight: function(){
		$('#program').append($('#topiclabel'));
		$('.highlight').each(function(){
			$(this).replaceWith($(this).html());
		});
		$('#topiclabel').hide();
		$('input[name=label]').val(this.id);
	},
	
	mouseover: function(){
		var container = $(this).parents('div.p').children('p');
		var contents = container.html();
       	var start = $(this).attr('topic:start');
        var end = $(this).attr('topic:end');
        container.html(contents.slice(0,start) + '<span class="highlight">' + contents.slice(start,end) + '</span>' + contents.slice(end));
	},
}

$(document).ready(function(){

	// do selection
	$('div.p').mouseup(function(){
	
		var myRange = rangy.getSelection();

		if (myRange.collapsed)
			return;

    	var selection = myRange.saveCharacterRanges(this); 
	    var startOffset = selection[0].range.start;
	    var endOffset = selection[0].range.end;

        //console.log('start:' + startOffset + '   -- end : ' + endOffset);

		$('input[name=start]').val(startOffset);
		$('input[name=end]').val(endOffset);
		$('input[name=pid]').val(this.id);
		$(document).wrapSelection().addClass('highlight')
		$('.highlight').last().append($('#topiclabel'));
		$('#topiclabel').show();
		$('input[name=label]').focus();
	});
  
  	//hide selection, only if where not clicking on an input
	$(document).mousedown(function(event){
		if(!$(event.target).is('p'))
			return;
				
		Topic.hideHighlight();
	});
	
	//submit on enter
	$('#topiclabel input').keypress(function(e){
		if(e.which == 13) {
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
				newLabel.mouseover(Topic.mouseout)
					.mouseout(Topic.hideHighlight)
					.appendTo(element);
			}
			
			Topic.hideHighlight();
		},
	});
	
	//hovers for topics
	$('.topic').hover(Topic.mouseover, Topic.hideHighlight);
	
	
	$( "input[name=label]" ).autocomplete({
			source: "/topic/getTopics/"
	});
});