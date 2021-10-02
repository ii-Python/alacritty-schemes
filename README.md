# alacritty-schemes
Colorscheme Generator for Alacritty

---

The main purpose of this repository is to parse the Alacritty color schemes () and  
convert them to a `colors.yml` file for you to use.  

To get started, simply clone the repository, install `requests` and `bs4`,  
and launch `themes.py`. It will create a `colors.yml` if all goes well.

---

If you wish, you can minify the `schemes` section of `colors.yml` using a service  
like [OnlineYAMLTools](https://onlineyamltools.com/minify-yaml). If you do this,  
you can copy the resulting YAML, paste it in `colors.yml` and run `themes.py minified`  
to get a `colors.yml` file using your minified YAML.
