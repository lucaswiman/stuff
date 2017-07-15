DROP TABLE IF EXISTS mytable;
DROP TABLE IF EXISTS mytable_patches;

CREATE TABLE mytable(
  id SERIAL PRIMARY KEY,
  data JSON
);

CREATE TABLE mytable_patches(
  id SERIAL PRIMARY KEY,
  mytable_id integer,
  timestamp timestamp default current_timestamp,
  patch JSON
);


CREATE OR REPLACE FUNCTION diff_jsonpatch (old JSON, new JSON)
  RETURNS JSON
AS $$
  import jsonpatch, json
  return jsonpatch.make_patch(json.loads(old), json.loads(new)).to_string()
$$ LANGUAGE plpythonu;


-- https://stackoverflow.com/questions/1295795/how-can-i-use-a-postgres-triggers-to-store-changes
CREATE OR REPLACE FUNCTION process_mytable_audit() RETURNS TRIGGER AS $mytable_audit$
  BEGIN
    IF (TG_OP = 'DELETE') THEN
      INSERT INTO mytable_patches (mytable_id, patch) VALUES (OLD.id, diff_jsonpatch(OLD.data, 'null'::JSON));
      RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
      INSERT INTO mytable_patches (mytable_id, patch) VALUES (OLD.id, diff_jsonpatch(OLD.data, NEW.data));
      RETURN NEW;
    ELSIF (TG_OP = 'INSERT') THEN
      INSERT INTO mytable_patches (mytable_id, patch) VALUES (NEW.id, diff_jsonpatch('null'::JSON, NEW.data));
      RETURN NEW;
    END IF;
    RETURN NULL;
  END;
$mytable_audit$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS mytable_audit ON mytable;
CREATE TRIGGER mytable_audit
AFTER INSERT OR UPDATE OR DELETE ON mytable
    FOR EACH ROW EXECUTE PROCEDURE process_mytable_audit();
