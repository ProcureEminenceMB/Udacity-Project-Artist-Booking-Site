window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

function deleteVenue( venue_id ){

	fetch( '/venues/' + venue_id, {
		method: 'DELETE'
	}).then( ( response ) => {

		if( response.status != 200 ){

			alert( 'Could not delete venue!' );
			throw 'Failed';

		}else{

			return response.json();

		}

	}).then( ( data ) => {

		if( data.success ){

			window.location.href = '/';

		}else{

			alert( 'Could not delete venue!' );

		}

	}).catch( ( error ) => {

		console.log( error );

	});

}