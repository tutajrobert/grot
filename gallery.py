import os, time

html_head = open("gallery.txt").readlines()

def add_image(im_name, desc):
    html_image = '\n<div class="img">\n \
                  <a target="_blank" href="' + im_name + '">\n \
                  <img src="' + im_name + '" width="640" height="480" alt="' + desc + '">\n \
                  </a></div>\n'
    return html_image

dis_res = "Displacement results"
strain_res = "Strain results"
stress_res = "Stress results"

def save_gallery(proj_name, images_list, desc_list, input_file, version):
    gallery_file = open("results" + os.sep + proj_name + os.sep + proj_name + "_gallery.html", "w+")
    for i in html_head:
        gallery_file.write(i)
        if i[0:6] == "<html>":
            gallery_file.write("<title>GRoT> project gallery: " + proj_name + "</title>")
    gallery_file.write('<h2><span>Gallery page of project <i>' + proj_name + '</i></span></h2>')
    gallery_file.write('<p>Bitmap input file for this analysis: ' + proj_name + ".bmp")
    gallery_file.write("<br>Date of analysis (year/month/day): " + (time.strftime("%Y/%m/%d")) + " \
    <br><tt>GRoT></tt> version: " + version + '<br>Visit website of this wonderful simulation package: <a href="https://github.com/tutajrobert">github.com/tutajrobert</a>' + \
    "<p>If you prompted to probe the results in individual elements, you will find them in: eres.txt" +\
    "</p><p>Input file for this analysis is shown below:<br>")
    gallery_file.write(input_file)
    gallery_file.write('<h2><span>Results images</span></h2>')
    gallery_file.write("\n")
    for i in range(len(images_list)):
        html_image = add_image(images_list[i], desc_list[i])
        gallery_file.write(html_image)
    gallery_file.write("\n</body>\n</html>")
    gallery_file.close()
    print("\nCreated results gallery [{}_gallery.html] in {}".format(proj_name ,"results" + os.sep + proj_name + os.sep))