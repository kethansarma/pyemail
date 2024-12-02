q1 = """CREATE OR REPLACE FUNCTION notify_email()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM pg_notify('email_channel', NEW.id::TEXT);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;"""
q2 = """SELECT public.notify_email();"""