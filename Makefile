build:
	sed "s,OPENNGC_COMMIT,`cat .git/modules/OpenNGC/HEAD`,g" create_kstars_ngcic_template.py > create_kstars_ngcic.py
	python3 create_kstars_ngcic.py

clean:
	rm create_kstars_ngcic.py

