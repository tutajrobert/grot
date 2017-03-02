import os, time

html_head = open("gallery.txt").readlines()

def add_image(im_name, desc):	
    html_image = '\n<div class="img">\n \
                  <a target="_blank" href="' + im_name + '">\n \
                  <img src="' + im_name + '" width="640" height="480">\n \
                  </a>\n<div class="desc">' + desc + '</div>\n</div>\n'
    return html_image

dis_res = "Displacement results"
strain_res = "Strain results"
stress_res = "Stress results"
	
results_strings = {"disp_x" : dis_res,
                   "disp_y" : dis_res,
				   "disp_mag" : dis_res,
				   "eps_x" : strain_res,
				   "eps_y" : strain_res,
				   "gamma_xy" : strain_res,
				   "sig_x" : stress_res,
				   "sig_y" : stress_res,
				   "tau_xy" : stress_res,
				   "huber" : stress_res,
				   "sign_huber" : stress_res,
				   "deformed" : dis_res}
	
def save_gallery(proj_name, images_list, desc_list, input_file, version):
    gallery_file = open("results" + os.sep + proj_name + os.sep + proj_name + "_gallery.html", "w+")
    for i in html_head:
        gallery_file.write(i)
        if i[0:6] == "<html>":
            gallery_file.write("<title>GRoT> project gallery" + proj_name + "</title>")
    gallery_file.write('\n<img src="' + '..' + os.sep + '..' + os.sep + 'logo_grot.png" width="240px"></img>')
    gallery_file.write("<hr>")
    gallery_file.write('<h3>Gallery page of GRoT> project: <font color = "#F8870E">' + proj_name + '</font></h3>')
    gallery_file.write("<p>Date of analysis (year/month/day): " + (time.strftime("%Y/%m/%d")) + " \
	<br>GRoT> version: " + version + '<br>Visit website of this wonderful simulation package: <a href="https://tutajrobert.github.io/grot/">tutajrobert.github.io/grot</a>' +"<br><br>Input file for this analysis is shown below:")
    gallery_file.write('<code>' + input_file + '</code>')
    gallery_file.write('<hr><h3>Results images</h3>')
    gallery_file.write("\n")
    for i in range(len(images_list)):
        html_image = add_image(images_list[i], desc_list[i])
        gallery_file.write(html_image)
    gallery_file.write("\n</body>\n</html>")
    gallery_file.close()
    print("\nCreated results gallery [{}_gallery.html] in {}".format(proj_name ,"results" + os.sep + proj_name + os.sep))