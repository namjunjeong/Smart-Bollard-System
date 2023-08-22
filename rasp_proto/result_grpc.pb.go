// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.2.0
// - protoc             v4.23.1
// source: result.proto

package rasp_proto

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.32.0 or later.
const _ = grpc.SupportPackageIsVersion7

// ResultClient is the client API for Result service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type ResultClient interface {
	Require(ctx context.Context, in *Req, opts ...grpc.CallOption) (Result_RequireClient, error)
}

type resultClient struct {
	cc grpc.ClientConnInterface
}

func NewResultClient(cc grpc.ClientConnInterface) ResultClient {
	return &resultClient{cc}
}

func (c *resultClient) Require(ctx context.Context, in *Req, opts ...grpc.CallOption) (Result_RequireClient, error) {
	stream, err := c.cc.NewStream(ctx, &Result_ServiceDesc.Streams[0], "/Result/Require", opts...)
	if err != nil {
		return nil, err
	}
	x := &resultRequireClient{stream}
	if err := x.ClientStream.SendMsg(in); err != nil {
		return nil, err
	}
	if err := x.ClientStream.CloseSend(); err != nil {
		return nil, err
	}
	return x, nil
}

type Result_RequireClient interface {
	Recv() (*Res, error)
	grpc.ClientStream
}

type resultRequireClient struct {
	grpc.ClientStream
}

func (x *resultRequireClient) Recv() (*Res, error) {
	m := new(Res)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

// ResultServer is the server API for Result service.
// All implementations must embed UnimplementedResultServer
// for forward compatibility
type ResultServer interface {
	Require(*Req, Result_RequireServer) error
	mustEmbedUnimplementedResultServer()
}

// UnimplementedResultServer must be embedded to have forward compatible implementations.
type UnimplementedResultServer struct {
}

func (UnimplementedResultServer) Require(*Req, Result_RequireServer) error {
	return status.Errorf(codes.Unimplemented, "method Require not implemented")
}
func (UnimplementedResultServer) mustEmbedUnimplementedResultServer() {}

// UnsafeResultServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to ResultServer will
// result in compilation errors.
type UnsafeResultServer interface {
	mustEmbedUnimplementedResultServer()
}

func RegisterResultServer(s grpc.ServiceRegistrar, srv ResultServer) {
	s.RegisterService(&Result_ServiceDesc, srv)
}

func _Result_Require_Handler(srv interface{}, stream grpc.ServerStream) error {
	m := new(Req)
	if err := stream.RecvMsg(m); err != nil {
		return err
	}
	return srv.(ResultServer).Require(m, &resultRequireServer{stream})
}

type Result_RequireServer interface {
	Send(*Res) error
	grpc.ServerStream
}

type resultRequireServer struct {
	grpc.ServerStream
}

func (x *resultRequireServer) Send(m *Res) error {
	return x.ServerStream.SendMsg(m)
}

// Result_ServiceDesc is the grpc.ServiceDesc for Result service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var Result_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "Result",
	HandlerType: (*ResultServer)(nil),
	Methods:     []grpc.MethodDesc{},
	Streams: []grpc.StreamDesc{
		{
			StreamName:    "Require",
			Handler:       _Result_Require_Handler,
			ServerStreams: true,
		},
	},
	Metadata: "result.proto",
}