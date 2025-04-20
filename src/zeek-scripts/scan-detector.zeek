module ScannerDetector;

export {
    redef enum Notice::Type += {
        SuspiciousActivity
    };
}

global scan_tracker: table[addr] of count &default=0;
global scan_timeout: interval = 60secs;

function reset_tracker(): void {
    scan_tracker = table();
    schedule scan_timeout { reset_tracker(); };
}

event zeek_init() {
    schedule scan_timeout { reset_tracker(); };
}

event Conn::log_rec(rec: Conn::Info) {
    if ( rec$duration < 0.05sec ) {
        scan_tracker[rec$id$orig_h] += 1;
    }

    if ( scan_tracker[rec$id$orig_h] > 10 ) {
        NOTICE([$note=SuspiciousActivity,
                $msg=fmt("Potential scanner detected: %s (%d short conns)", rec$id$orig_h, scan_tracker[rec$id$orig_h]),
                $src=rec$id$orig_h]);
    }
}
