I want a Online Documentation mockup page, where forms for the restoration of archeological artifacts can be filled out, to mock filling fields in a database.

Generate me a HMTL document with JS and CCs, that should be maintainable, ideally dynamically created modular code, based around the appended jsons, that should be integrated in the JS part and be the core of the application, so the application can be changed by changing them.

Features:

1. Use The arrays in the thesaurus.json as dropdown options for the form elements with a key in it

2. Prefill the following fields, using thesaurus dropdown options if possible:

	1. Objektkennzeichnung

	2. Objektbeschreibung

	6. Untersuchung

	7. Probeentnahme

	8. Sicherheit & Arbeitsschutz

	9. Präventive Konservierung

	10. Verwendete Literatur

	11. Administrative Metadaten



3. Fields with bedingte Pflicht should contain a selectable element, that makes them Pflicht if marked.

4. All the  data in the forms should be able to be exported as JSON via button

5. There should be a validation if all Pflicht fields have been filled with an alarm message popping up if not, so there is no export.

6. Some form elements should be able to be added multiple times and also deleted. They are marked with multiple = true in the JSON

7. There should be another button prefilling the not already prefilled fields, also using the thesaurus.json if possible