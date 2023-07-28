## Folder structure 🗄️

- [anwesha](./anwesha/) :- This app contains all the configurations related files.❗❗.env file should be placed here also cloud storage configurations should be kept here.
- [CA](./CA/) :- This Django app contains code for `/campasambassador/` endpoint APIs.This apis are responsible for CA authentication,registration and management of CA points.
- [event](./event/) :- This Django app contains code for `/event/` endpoint APIs.This apis are responsible for fetching event details , single/ team event registration and QR code verification and entry.
- [sponsor](./sponsor/) :- This Django app contains code for `/sponsors/` APIs. This apis are responsible for fetching details of event sponsors.
- [static](./static/) :- This is for storing static files like profile images and QR codes.
- [user](./user/) :- This app contains code for `/user/` APIs. This apis are responsible for user registration,auth and  QR code regeneration.