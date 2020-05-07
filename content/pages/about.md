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
