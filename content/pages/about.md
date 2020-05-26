Title: About Me
Slug: about

<script type="application/ld+json">
{
"@context": "http://www.schema.org",
"@type": "Person",
"@id": "https://www.cameronmacleod.com/#person",
"name": "Cameron MacLeod",
"nationality": "British",
"alumniOf": [
	{
	 "@type": "CollegeOrUniversity",
	 "name": "University of Edinburgh",
	 "sameAs": "https://en.wikipedia.org/wiki/University_of_Edinburgh"
	}
],
"gender": "Male",
"Description": "Developer",
"url": "https://www.cameronmacleod.com",
"image": "https://www.cameronmacleod.com/images/profile.jpg",
"sameAs": [
	"https://twitter.com/notexactlyawe",
	"https://www.linkedin.com/in/cameronjohnmacleod/",
	"https://github.com/notexactlyawe",
	"https://angel.co/u/cameron-macleod-2",
	"https://stackoverflow.com/users/1546934/cjm",
	"https://www.flickr.com/people/rotor132"
	]
}
</script>

<script>
var email;

function add_mailto() {
  const elem = document.getElementById("emailclick");
  elem.href = `mailto:${email}`;
}

function replace_email() {
  // short function to prevent spambots from scraping my email
  const domain = "gmail.com";
  const name = [16, 30, 18, 16, 31, 22, 28, 23, 66, 68, 67];
  const xor_with = 115;
  let constructed = "";
  name.forEach(function(i) {
    constructed += String.fromCharCode(i ^ xor_with);
  })
  email = `${constructed}@${domain}`;
  const elem = document.getElementById("emailclick");
  elem.text = email;
  // need to delay this so that the mailto gets added after the click, otherwise
  // an unexpected mail dialogue will popup
  window.setTimeout(add_mailto, 100);
}
</script>

Hello! I'm Cameron, and this is my personal blog. New posts come out sometimes, and usually are on technical topics related to software development. If you want to contact me you can email me at <a href="#" id="emailclick" onclick="replace_email()">click to reveal</a> or find me in one of the sidebar links.

I'm just about to graduate from the University of Edinburgh with a degree in computer science and will be joining Google as an associate product manager in August. Previously I've done a few internships in software development (see my [CV](/cv.pdf)).

In my free time you can find me coding, writing, playing the bass or more likely starting projects that I will never finish.

This is my personal site and views presented here do not necessarily reflect those of my employer.

<!-- Begin Mailchimp Signup Form -->
<div id="mc_embed_signup">
	<form action="https://cameronmacleod.us18.list-manage.com/subscribe/post?u=ee6251a0e7d61c20060602217&amp;id=f541a0bdba" method="post" id="mc-embedded-subscribe-form" name="mc-embedded-subscribe-form" class="validate" target="_blank" novalidate>
		<div id="mc_embed_signup_scroll">
			<h2>No spam, just new posts. Choose what you receive and unsubscribe whenever.</h2>
			<div class="mc-field-group">
				<label for="mce-EMAIL">Email Address </label>
				<input type="email" value="" name="EMAIL" class="required email" id="mce-EMAIL">
			</div>
			<div class="mc-field-group input-group">
			    <strong>Which posts do you want to receive?</strong>
			    <ul>
						<li><input type="checkbox" value="1" name="group[4534][1]" id="mce-group[4534]-4534-0" checked><label for="mce-group[4534]-4534-0">Blog posts</label></li>
						<li><input type="checkbox" value="2" name="group[4534][2]" id="mce-group[4534]-4534-1" checked><label for="mce-group[4534]-4534-1">Tutorials</label></li>
					</ul>
			</div>
			<div id="mce-responses" class="clear">
				<div class="response" id="mce-error-response" style="display:none"></div>
				<div class="response" id="mce-success-response" style="display:none"></div>
			</div>    <!-- real people should not fill this in and expect good things - do not remove this or risk form bot signups-->
			<div style="position: absolute; left: -5000px;" aria-hidden="true"><input type="text" name="b_ee6251a0e7d61c20060602217_f541a0bdba" tabindex="-1" value=""></div>
			<div class="clear"><input type="submit" value="Subscribe" name="subscribe" id="mc-embedded-subscribe" class="button"></div>
		</div>
	</form>
</div>
<script type='text/javascript' src='//s3.amazonaws.com/downloads.mailchimp.com/js/mc-validate.js'></script><script type='text/javascript'>(function($) {window.fnames = new Array(); window.ftypes = new Array();fnames[0]='EMAIL';ftypes[0]='email';fnames[1]='FNAME';ftypes[1]='text';fnames[2]='LNAME';ftypes[2]='text';fnames[3]='ADDRESS';ftypes[3]='address';fnames[4]='PHONE';ftypes[4]='phone';fnames[5]='BIRTHDAY';ftypes[5]='birthday';}(jQuery));var $mcj = jQuery.noConflict(true);</script>
<!--End mc_embed_signup-->
