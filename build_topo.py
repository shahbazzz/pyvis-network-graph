import sys,os
sys.path.append("/home/advithj/unittest/pytest/lib/python3.6/site-packages/topo/")
from pyvis.network import Network
from time import time

def generate_topo(GlobalVariables, *args, **kwargs):
	nt = Network(height="490px", width="100%", bgcolor="#FFF", directed=True,  notebook=True, heading="")
	size_multiplier = 1
	if "scale" in kwargs:
		size_multiplier = kwargs["scale"]

	try:
		# NE1_IP
		NE_list = list()
		LK_list = list()
		Link_list = list()
		attr_list = dir(GlobalVariables)
		for attr in attr_list:
			if attr=="L3_Testset_IP":
				testset_label = GlobalVariables.L3_Testset_IP
			if attr.startswith("NE") or attr.startswith("PT"):
				chunks = attr.split("_")
				if len(chunks) == 2 and chunks[0].startswith("NE") and chunks[1]=="IP":
					NE_list.append({"type":"node", "type":"node", "id":chunks[0], "label":getattr(GlobalVariables,attr),"x":-300+x1,"y":100+y1, "title":getattr(GlobalVariables,attr)})
					x1 = x1 +300
					ne = ne+1
				elif len(chunks) ==2 and chunks[0].startswith("PT") and chunks[1]=="IP":
					NE_list.append({"type":"node", "id":chunks[0], "label": getattr(GlobalVariables,attr),"x":-150+x2,"y":400, "title": getattr(GlobalVariables,attr)})
					x2 = x2 + 300
					pt = pt+1
				else:
					if "#" not in getattr(GlobalVariables, attr):
						continue
					to = chunks[1]
					if chunks[1] == "UNI":
						to = "TS_" + chunks[0]
						NE_list.append({"type":"ts", "id": to, "label": testset_label, "x": -300+tsx , "y": -100,
						"title": getattr(GlobalVariables, attr)})
						tsx +=300
					Link_list.append({
					"from": chunks[0],
					"to": to,
					"label_from": chunks[0]+" ("+getattr(GlobalVariables,attr).split("#")[0]+")",
					"label_to": to+" ("+getattr(GlobalVariables,attr).split("#")[1]+")"
					})
		correction_y = 0
		if ne>2 and pt==0:
			correction_y = 300

		for NE in NE_list:
			if NE["type"]=="ts":
				color="#1e4c1b"
				shape="box"
				rel = NE["id"].split("_")[1]
				x_axis = NE["x"],
				y_axis = NE["y"],
				for ele in NE_list:
					if ele["id"]==rel:
						corr=0
						if int(ele['id'][2:])% 2==0:
							corr = correction_y
						if ele["y"] ==100 and corr==0:
							x_axis = ele["x"]
							y_axis = ele["y"] -200 - corr
						else:
							x_axis = ele["x"]
							y_axis = ele["y"]+200 +corr
			else:
				color="#366dbf"
				shape="box"
				x_axis = NE["x"]
				y_axis = NE["y"]
				if NE["id"].startswith("NE"):
					if int(NE['id'][2:])% 2==0:
						y_axis = int(y_axis) + correction_y
			nt.add_node(
				NE["id"],
				shape=shape,
				color=color,
				label=f'\n{NE["id"]}\n{NE["label"]}\n',
				x=x_axis,
				y=y_axis,
				title=NE["id"],
				group=1
			)
		for link in Link_list:
			nt.add_edge(
				link["from"],
				link["to"],
				title=f"{link['label_from']}---{link['label_to']}",
				label=f"{link['label_from']}---{link['label_to']}"
				#color="#CDA"
			)
		nt.set_edge_smooth('dynamic')

		nt.set_options('''
		var options = {
		  "autoResize": true,
		  "nodes": {
		   "physics":false,
		    "borderWidth": 0,
		    "borderWidthSelected": 2,
		   "font": {
                      "color": "white",
		      "size": 14
		   }
		  },
		  "edges": {
		    "arrows": {
		      "to": {
			"enabled": true,
			"scaleFactor": 0
		      }
		    },
		    "arrowStrikethrough": true,
		    "color": {
		      "color": "#2f966b",
		      "hover": "#2f966b",
		      "highlight": "#2f966b",
		      "inherit": false
		    },
		    "font": {
		      "color": "#000",
		      "strokeWidth": 0,
		      "size": 12,
		      "align": "top"
		    },
		    "hoverWidth": 1.1,
		    "labelHighlightBold": true,
		    "scaling": {
		      "min": 0,
		      "max": 0,
		      "label": {
			"min": 4,
			"max": 27,
			"maxVisible": 44
		      }
		    },
		    "selectionWidth": 1.3
		  },
		  "interaction": {
		    "multiselect": true,
		    "navigationButtons": true,
		    "tooltipDelay": 75
		  },
		  "physics": {
		  }
		}
		''')
		file_time = str(time())[:10]
		file_time = "try"
		file_ref = f"/web/tomcat/webapps/SASFiles/LogFiles/{file_time}.html"
		file_iref = f"/SASFiles/LogFiles/{file_time}.html"
		file_iref1 = f"/web/tomcat/webapps/SASFiles/LogFiles/{file_time}.html"
		nt.show(file_ref)
		with open (file_iref1) as fp:
			content = fp.readlines()
		content = [x.strip() for x in content]
		data = ""
		for line in content:
			if not line.startswith("//"):
				data = f"{data}{line}"
		with open (file_iref1,"w") as fp:
			fp.write(data)
		os.remove(file_ref)
		#print(f"<iframe name=\"topology_class[]\" src=\"{file_iref}\" width=\"100%\" height=\"500px\" onfocusin=\"this.contentWindow.network.fit();\"></iframe>")
		print(f"<div style=\"width:100%;height:500px\"; onfocus=\"this.getElementById('mynetwork').fit()\" >{data}</div>")
	except Exception as e:
		print(f"Error occured while building topography:{e}")

