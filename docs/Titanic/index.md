# Titanic Disaster Analysis
## A Data-Driven Investigation of the 1912 Maritime Tragedy

This analysis explores the passenger data from the RMS Titanic disaster, examining survival patterns and social dynamics aboard history's most famous shipwreck. Through statistical analysis and data visualization, we'll investigate:

- Passenger demographics and survival rates
- The impact of social class on survival
- Gender and age-based survival patterns
- Family dynamics during the disaster
- Lifeboat allocation and evacuation patterns

The dataset contains information on 1,309 passengers, including details about their age, gender, ticket class, fare paid, and survival status. This analysis aims to uncover the human stories behind the numbers and understand the factors that influenced survival on that fateful night of April 15, 1912.

Let's begin our journey through the data...

<a href="titanic_en.ipynb" class="md-button md-button--primary"> Link to the notebook</a>

<iframe
    id="content"
    src="titanic_en_as_report.html"
    width="100%"
    style="border: 1px solid black;overflow: hidden;">
</iframe>
<script>
function resizeIframeToContent(iframe) {
    const newHeight = iframe.contentWindow.document.documentElement.scrollHeight + 50;
    iframe.style.height = newHeight + 'px';
    iframe.contentDocument.body.style.overflow = 'hidden';
}
window.addEventListener('load', function() {
    const iframe = document.getElementById('content');
    resizeIframeToContent(iframe);
});
window.addEventListener('resize', function() {
    const iframe = document.getElementById('content');
    resizeIframeToContent(iframe);
});
</script>