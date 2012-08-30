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
	
		var myRange = $(document).getRangeAt();
		
		if (myRange.collapsed)
			return;
	
		$('input[name=start]').val(myRange.startOffset);
		$('input[name=end]').val(myRange.endOffset);
		$('input[name=pid]').val(this.id);
		$(document).wrapSelection().addClass('highlight').append($('#topiclabel'));
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
				var newLabel = $('<div class="topic" id="'+data.id+'"  topic:start="'+data.start+'" topic:end="'+data.end+'">'+data.label+'</div>');
				newLabel.mouseover(Topic.mouseout)
					.mouseout(Topic.hideHighlight)
					.appendTo(element);
			}
			
			Topic.hideHighlight();
		},
	});
	
	//hovers for topics
	$('.topic').hover(Topic.mouseover, Topic.hideHighlight);
});