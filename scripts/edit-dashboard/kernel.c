// macOS: identity checks only; no lock acquisition or process control.
#include <libproc.h>
#include <sys/proc_info.h>
#include <sys/stat.h>
#include <IOKit/IOKitLib.h>
#include <CoreFoundation/CoreFoundation.h>
#include <stdlib.h>
#include <mach/mach_time.h>
#include <unistd.h>
double idle_seconds(void) {
    io_service_t s=IOServiceGetMatchingService(kIOMainPortDefault,IOServiceMatching("IOHIDSystem"));
    if (!s) return -1;
    CFTypeRef v=IORegistryEntryCreateCFProperty(s, CFSTR("HIDIdleTime"),kCFAllocatorDefault,0);
    IOObjectRelease(s); int64_t ns=-1;
    if(v){if(CFGetTypeID(v)==CFNumberGetTypeID())CFNumberGetValue(v,kCFNumberSInt64Type,&ns);CFRelease(v);}
    return ns<0?-1:(double)ns/1e9;
}
int matches(int pid,double record,int fd) {
    struct proc_bsdinfo b; struct stat st;
    if(pid<1||proc_pidinfo(pid,PROC_PIDTBSDINFO,0,&b,sizeof(b))!=sizeof(b)||fstat(fd,&st))return 0;
    if(b.pbi_start_tvsec+b.pbi_start_tvusec/1e6>record+0.005)return 0;
    struct proc_fdinfo entries[512]; int bytes=proc_pidinfo(pid,PROC_PIDLISTFDS,0,entries,sizeof(entries));
    for(int i=0;i<bytes/(int)sizeof(*entries);i++)if(entries[i].proc_fdtype==PROX_FDTYPE_VNODE){
        struct vnode_fdinfo v;
        if(proc_pidfdinfo(pid,entries[i].proc_fd,PROC_PIDFDVNODEINFO,&v,sizeof(v))==sizeof(v)
           &&v.pvi.vi_stat.vst_ino==st.st_ino&&v.pvi.vi_stat.vst_dev==st.st_dev)return 1;
    }
    return 0;
}
// Bounded benchmark only. Never enumerate unrelated processes.
int cost(int pid, double *dest) {
    struct rusage_info_v2 r={0}; struct proc_bsdinfo b={0};struct proc_taskinfo t={0};
    if(proc_pidinfo(pid,PROC_PIDTBSDINFO,0,&b,sizeof(b))!=sizeof(b)){dest[0]=dest[1]=dest[2]=-1;return -1;}
    if(proc_pid_rusage(pid,RUSAGE_INFO_V2,(rusage_info_t*)&r)==0){
      dest[0]=(r.ri_user_time+r.ri_system_time)/1e9;dest[1]=r.ri_resident_size;
      dest[2]=r.ri_phys_footprint;dest[3]=(r.ri_child_user_time+r.ri_child_system_time)/1e9;
    }else if(proc_pidinfo(pid,PROC_PIDTASKINFO,0,&t,sizeof(t))==sizeof(t)){
      dest[0]=(t.pti_total_user+t.pti_total_system)/1e9;dest[1]=t.pti_resident_size;dest[2]=-1;
    }else dest[0]=dest[1]=dest[2]=-1;
    mach_timebase_info_data_t tb;mach_timebase_info(&tb);double ratio=(double)tb.numer/tb.denom;
    if(dest[0]>=0)dest[0]*=ratio;
    dest[3]*=ratio;
    return (int)b.pbi_ppid;
}
