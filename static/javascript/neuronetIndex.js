
function sellArtwork(artworkId) {
    fetch('/fellowship/sell-artwork', {
        method: 'POST',
        body: JSON.stringify({ artworkId: artworkId})
    }).then((_res) => {
        window.location.href = "/fellowship/inventory";
    });
}

function buyArtwork(artworkId) {
    fetch('/fellowship/buy-artwork', {
        method: 'POST',
        body: JSON.stringify({ artworkId: artworkId})
    }).then((_res) => {
        window.location.href = "/fellowship/market";
    });
}

function nextDay() {
    fetch('/fellowship/next-day', {
        method: 'POST',
        body: JSON.stringify({})
    }).then((_res) => {
        window.location.href = "/fellowship/myAdmin";
    });
}

function genCode() {
    fetch('/fellowship/gen-code', {
        method: 'POST',
        body: JSON.stringify({})
    }).then((_res) => {
        window.location.href = "/fellowship/myAdmin";
    });
}



$(function(){
    $('a').each(function(){
        if ($(this).prop('href') == window.location.href) {
            $(this).addClass('active'); $(this).parents('li').addClass('active');
        }
    });
});



function openPopup(popup) {
	/* Open popup and make accessible screen readers */
	$(popup).show().attr("aria-hidden", "false");
	/* Focus on element to guide screen readers to popup */
	$("#closePopup").focus();
}

function closePopup(popup) {
	/* Close popup and hide from screen readers */
	$(popup).hide().attr("aria-hidden", "true");
	/* Focus screen readers back to button */
	$("#openPopup").focus();
}



$(function(){
	$('#vitalSubmitButton').click(function(event){
		$.ajax({
			data:{ 
            maxHP: $('#maxHPInput').val(),
            maxOverrideHP: $('#maxOverHPInput').val(),
            },
			type: 'POST',
            url: '/submitVitals',
        })
        .done(function(data) {

            if(data.maxOverrideHP > 0){
                $('#sumMaxHP').html(data.maxOverrideHP + ' (' + data.maxHP + ')')
                $('#quickMaxHP').html(data.maxOverrideHP)
            } else {
                $('#sumMaxHP').html(data.maxHP)
                $('#quickMaxHP').html(data.maxHP)
            }

            if(data.tmpHP > 0 ){
                $('#sumCurrentHP').html(data.newHP + ' (' + data.tmpHP + ')')
            }else{
                $('#sumCurrentHP').html(data.newHP)
            }

            $('#quickCurrentHP').html(data.newHP + data.tmpHP)
           
      });
      event.preventDefault();
      });
});


$(function(){
	$('#healButton').click(function(event){
		$.ajax({
			data:{ 
            healHP: $('#adjustHPInput').val(),
            },
			type: 'POST',
            url: '/healVitals',
        })
        .done(function(data) {
            $('#adjustHPInput').val(0)

            if(data.tmpHP > 0 ){
                $('#sumCurrentHP').html(data.newHP + ' (' + data.tmpHP + ')')
            }else{
                $('#sumCurrentHP').html(data.newHP)
            }
            
            $('#quickCurrentHP').html(data.newHP + data.tmpHP)
           
      });
      event.preventDefault();
      });
});

$(function(){
	$('#damageButton').click(function(event){
		$.ajax({
			data:{ 
            damageHP: $('#adjustHPInput').val(),
            },
			type: 'POST',
            url: '/damageVitals',
        })
        .done(function(data) {
            $('#adjustHPInput').val(0)
            $('#sumTmpHP').val(data.tmpHP)

            if(data.tmpHP > 0 ){
                $('#sumCurrentHP').html(data.newHP + ' (' + data.tmpHP + ')')
            }else{
                $('#sumCurrentHP').html(data.newHP)
            }
            
            $('#quickCurrentHP').html(data.newHP + data.tmpHP)
           
      });
      event.preventDefault();
      });
});


$(function(){
	$('#acSubmitButton').click(function(event){
		$.ajax({
			data:{ 
            baseAC: $('#baseACInput').val(),
            ability1: $('#ability1Dropdown').val(),
            ability2: $('#ability2Dropdown').val(),
            overrideAC: $('#overrideACInput').val(),
            },
			type: 'POST',
            url: '/submitAC',
        })
        .done( function(){
            window.location.reload()
      });
      event.preventDefault();
      });
});

$(function(){
	$('#quickBarSubmitButton').click(function(event){
		$.ajax({
			data:{ 
            walkSpeed: $('#walkSpeedInput').val(),
            flySpeed: $('#flySpeedInput').val(),
            swimSpeed: $('#swimSpeedInput').val(),
            climbSpeed: $('#climbSpeedInput').val(),
            initOverride: $('#initOverrideInput').val(),
            profBonus: $('#profInput').val(),
            },
			type: 'POST',
            url: '/submitQuickBar',
        })
        .done( function(){
            window.location.reload()
      });
      event.preventDefault();
      });
});

$(function(){
	$('#savesSubmitButton').click(function(event){
		$.ajax({
			data:{ 
            strProf: $('#strSaveProf').is(":checked"),
            strOverride: $('#strSaveOverrideInput').val(),
            dexProf: $('#dexSaveProf').is(":checked"),
            dexOverride: $('#dexSaveOverrideInput').val(),
            conProf: $('#conSaveProf').is(":checked"),
            conOverride: $('#conSaveOverrideInput').val(),
            intProf: $('#intSaveProf').is(":checked"),
            intOverride: $('#intSaveOverrideInput').val(),
            wisProf: $('#wisSaveProf').is(":checked"),
            wisOverride: $('#wisSaveOverrideInput').val(),
            chaProf: $('#chaSaveProf').is(":checked"),
            chaOverride: $('#chaSaveOverrideInput').val(),
            },
			type: 'POST',
            url: '/submitSaves',
        })
        .done(function(data) {

            wwindow.location.reload()
      });
      event.preventDefault();
      });
});

$(function(){
	$('#infoSubmitButton').click(function(event){
		$.ajax({
			data:{ 
            nameInfo: $('#nameInput').val(),
            speciesInfo: $('#speciesInput').val(),
            ageInfo: $('#ageInput').val(),
            homeworldInfo: $('#homeworldInput').val(),
            },
			type: 'POST',
            url: '/submitInfo',
        })
        .done(function(data) {

            window.location.href = "/";
      });
      event.preventDefault();
      });
});

$(function(){
	$('#abilitySubmitButton').click(function(event){
		$.ajax({
			data:{ 
            strBase: $('#strInput').val(),
            strOverride: $('#strOverrideInput').val(),
            dexBase: $('#dexInput').val(),
            dexOverride: $('#dexOverrideInput').val(),
            conBase: $('#conInput').val(),
            conOverride: $('#conOverrideInput').val(),
            intBase: $('#intInput').val(),
            intOverride: $('#intOverrideInput').val(),
            wisBase: $('#wisInput').val(),
            wisOverride: $('#wisOverrideInput').val(),
            chaBase: $('#chaInput').val(),
            chaOverride: $('#chaOverrideInput').val(),
            },
			type: 'POST',
            url: '/submitAbilities',
        })
        .done(function(data) {

            window.location.href = "/";
      });
      event.preventDefault();
      });
});



$(function(){
	$('#sumTmpHP').on("blur", function(){
		$.ajax({
			data:{ 
            tmpHP: $('#sumTmpHP').val(),
            },
			type: 'POST',
            url: '/tmpVitals',
        })
        .done(function(data) {
            $('#sumTmpHP').val(data.tmpHP)
            
            if(data.tmpHP > 0 ){
                $('#sumCurrentHP').html(data.currentHP + ' (' + data.tmpHP + ')')
            }else{
                $('#sumCurrentHP').html(data.currentHP)
            }
            
            $('#quickCurrentHP').html(data.currentHP + data.tmpHP)
           
      });
      event.preventDefault();
      });
});