CREATE TABLE "Users" (
	"user_id" serial NOT NULL,
	"email" TEXT NOT NULL UNIQUE,
	"password" TEXT NOT NULL,
	"role_id" integer NOT NULL DEFAULT '1',
	"is_active" BOOLEAN NOT NULL DEFAULT 'True',
	CONSTRAINT "Users_pk" PRIMARY KEY ("user_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Roles" (
	"role_id" serial NOT NULL,
	"role_name" TEXT NOT NULL UNIQUE,
	CONSTRAINT "Roles_pk" PRIMARY KEY ("role_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Notes" (
	"note_id" serial NOT NULL,
	"user_id" integer NOT NULL,
	"date" integer NOT NULL,
	"note" TEXT NOT NULL,
	CONSTRAINT "Notes_pk" PRIMARY KEY ("note_id")
) WITH (
  OIDS=FALSE
);



ALTER TABLE "Users" ADD CONSTRAINT "Users_fk0" FOREIGN KEY ("role_id") REFERENCES "Roles"("role_id");


ALTER TABLE "Notes" ADD CONSTRAINT "Notes_fk0" FOREIGN KEY ("user_id") REFERENCES "Users"("user_id");

